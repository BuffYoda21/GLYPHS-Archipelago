from enum import Enum
from typing import Dict, List, Optional, Set
import asyncio
import traceback
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from .citra import CitraInterface, CitraException
from .triple import TripleInterface, TripleException
from ..world import OoT3DWorld

citra = CitraInterface()
triple = TripleInterface()
triple_addr = ""

class AppConnectionStatus(Enum):
    NOT_CONNECTED = 0
    INCOMPATIBLE_VERSION = 1
    WAITING_ON_RANDOMIZER_APP = 2
    AUTHENTICATING = 3
    INVALID_SLOT = 4
    WAITING_TO_CONNECT_TO_MULTIWORLD = 5
    WAITING_ON_MULTIWORLD_DATA = 6
    CONNECTED = 7

def bytes_or(a: bytes, b: bytes) -> bytes:
    return bytes([x | y for x,y in zip(a,b)])

class OoT3DCommandProcessor(ClientCommandProcessor):
    pass

    ## Retail 3DS support not implemented
    # 
    # def _cmd_3ds(self, address):
    #     """Connect to a real 3ds"""
    #     global triple_addr
    #     if triple_addr == "":
    #        triple_addr = address
    #     else:
    #         self.output("Already connected to a 3ds")
    # 
    # def _cmd_3dsdisconnect(self):
    #     """Disconnect from a 3ds"""
    #     global triple_addr
    #     if triple_addr == "":
    #         self.output("Not currently connected to a 3ds")
    #     else:
    #         self.output(f"Disconnected from {triple_addr}.")
    #         triple_addr = ""
    # 
    # def _cmd_3dstimeout(self, timeout):
    #     """Set timeout (in connection attempts) until giving up connection to 3ds (default 200000)"""
    #     global triple
    #     if triple.set_timeout(timeout):
    #         self.output(f"Successfully set timeout to {timeout} attempts")
    #     else:
    #         self.error(f"Invalid timeout: {timeout}")

class OoT3DClientContext(CommonContext):
    command_processor = OoT3DCommandProcessor
    game: Optional[str] = "Ocarina of Time 3D"
    items_handling: Optional[int] = 0b101 # receive remote items and starting inventory
    want_slot_data: bool = True

    interface = None
    interface_connected: bool
    app_connection_status: AppConnectionStatus
    authenticating: bool
    server_connected: bool
    initial_delay: bool
    slot_data: Optional[Dict[str, any]]
    save_ptr: int
    event_flags_ptr: int
    course_flags_ptr: int
    minigame_ptr: int
    event_flags: bytes
    course_flags: List[bytes]
    minigame_flags: int
    course: int
    stage: int
    to_hint: List[int]
    invalid: bool
    last_error: str
    show_citra_connect_message: bool
    show_triple_connected_message: bool

    DATA_VERSION: int = 1
    AP_HEADER_LOCATION: int = 0x6fe5f8
    RANDOMIZER_APP_HEADER_LOCATION: int = 0x4f8000 # may change in the future idk
    SAVES_LOCATION: int = 0x711de8
    EVENTS_LOCATION: int = 0x70b728
    COURSES_LOCATION: int = 0x70c8e0
    MINIGAME_LOCATION: int = 0x70d858
    GAME_LOCATION: int = 0x709df8
    TASK_MAIN_GAME_VTABLE: int = 0x6d1db4

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.interface_connected = False
        self.app_connection_status = AppConnectionStatus.NOT_CONNECTED
        self.server_connected = False
        self.authenticating = False
        self.initial_delay = True
        self.slot_data = None
        self.course_flags = []
        self.ravio_scouted = False
        self.to_hint = []
        self.invalid = False
        self.last_error = ""
        self.show_citra_connect_message = True
        self.show_triple_connected_message = True

    def run_gui(self) -> None:
        from kvui import GameManager

        class OoT3DManager(GameManager):
            base_title: str = "Archipelago Ocarina of Time 3D Client"

        self.ui = OoT3DManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    
    def error(self, error: str) -> None:
        if error != self.last_error:
            logger.error(error)
            self.last_error = error
        self.invalid = True
    
    async def citra_connect(self) -> None:
        if self.show_citra_connect_message:
            logger.info("Connecting to emulator...")
        self.show_citra_connect_message = False
        self.interface_connected = False
        if not await self.interface.connect():
            await asyncio.sleep(1)
        else:
            self.interface_connected = True
            self.initial_delay = True
            if self.server_connected:
                logger.info("Emulator connected")
            else:
                logger.info("Emulator connected, but not yet connected to the multiworld")
    
    async def validate_rom(self) -> None:
        # logger.info("read memory %s" % ((await self.interface.read(self.RANDOMIZER_APP_HEADER_LOCATION, 27))))
        # logger.info("app_connection_status %s" % (self.app_connection_status.name))
        if (await self.interface.read(self.RANDOMIZER_APP_HEADER_LOCATION, 8)) == b"OOT3RAND":
            await self.connect_app()   
            return
        self.app_connection_status = AppConnectionStatus.NOT_CONNECTED
            
        if (await self.interface.read(self.AP_HEADER_LOCATION, 4)) != b"ARCH":
            self.error("Running incompatible or incorrectly patched game.")
        elif (await self.interface.read_u32(self.AP_HEADER_LOCATION + 0x4)) < self.DATA_VERSION:
            self.error("Version mismatch: update your oot3drandomizer library and re-patch.")
        elif (await self.interface.read_u32(self.AP_HEADER_LOCATION + 0x4)) > self.DATA_VERSION:
            self.error("Version mismatch: update your apworld and restart the client.")
        else:
            name = await self.interface.read(self.AP_HEADER_LOCATION + 0x10, 0x40)
            end = name.find(0)
            if end != -1:
                name = name[:end]
            self.auth = name.decode("utf-8")
    
    async def connect_app(self) -> None:
        if self.app_connection_status == AppConnectionStatus.NOT_CONNECTED:
            logger.info("Connected to the OoT3D Randomizer app")
            
        if (await self.interface.read(self.RANDOMIZER_APP_HEADER_LOCATION + 0x8, 1)) != self.DATA_VERSION.to_bytes(1, "little"):
            if self.app_connection_status != AppConnectionStatus.INCOMPATIBLE_VERSION:
                self.error("Version mismatch: update and restart your randomzier app and/or client.")
                self.app_connection_status = AppConnectionStatus.INCOMPATIBLE_VERSION
        
        elif (await self.interface.read(self.RANDOMIZER_APP_HEADER_LOCATION + 0x9, 1)) == b'\x00': # randomizer app is not listening
            if self.app_connection_status != AppConnectionStatus.WAITING_ON_RANDOMIZER_APP:
                logger.info("Enter your slot name and select \"Connect and Generate\" in the Randomizer App to send randomizer data")
                self.app_connection_status = AppConnectionStatus.WAITING_ON_RANDOMIZER_APP

        elif not self.server or self.server.socket.closed:
            if self.app_connection_status != AppConnectionStatus.WAITING_TO_CONNECT_TO_MULTIWORLD:
                logger.info("Waiting to connect to the multiworld...")
                self.app_connection_status = AppConnectionStatus.WAITING_TO_CONNECT_TO_MULTIWORLD

        elif not self.server_connected:
            if self.app_connection_status != AppConnectionStatus.AUTHENTICATING:
                recv_slot = (await self.interface.read(self.RANDOMIZER_APP_HEADER_LOCATION + 0x0A, 16)).split(b'\x00', 1)[0].decode()
                if self.auth != recv_slot:
                    self.auth = recv_slot
                    self.app_connection_status = AppConnectionStatus.AUTHENTICATING
            elif self.app_connection_status != AppConnectionStatus.INVALID_SLOT and not self.authenticating and not self.auth:
                    self.error("Invalid Slot: Double check your spelling? (\"%s\" does not match any valid slot in the multiworld)" % (self.auth))
                    self.app_connection_status = AppConnectionStatus.INVALID_SLOT
                    self.auth = None
        
        elif not self.slot_data:
            if self.app_connection_status != AppConnectionStatus.WAITING_ON_MULTIWORLD_DATA:
                logger.info("Waiting for the multiworld to send slot data...")
                self.app_connection_status = AppConnectionStatus.WAITING_ON_MULTIWORLD_DATA

        elif self.app_connection_status != AppConnectionStatus.CONNECTED:
            logger.info("Sending slot data to the OoT3D Randomizer app...")
            self.app_connection_status = AppConnectionStatus.CONNECTED
            await self.send_slot_data()
    
    async def send_slot_data(self) -> None:
        pass
    
    async def validate_save(self) -> None:
        self.save_ptr = 0
        all_saves_ptr = await self.interface.read_u32(self.SAVES_LOCATION)
        if all_saves_ptr != 0:
            self.save_ptr = await self.interface.read_u32(all_saves_ptr + 0x14)
        if all_saves_ptr == 0 or self.save_ptr == 0 or await self.interface.read_u32(self.save_ptr + 0x1600) != 0:
            self.invalid = True
            self.last_error = ""
        elif await self.interface.read(self.save_ptr + 0xde0, 4) == b"\0\0\0\0":
            self.error("The loaded save file is not an Archipelago save file. Choose a different save file.")
        elif await self.interface.read(self.save_ptr + 0xde0, 4) != b"ARCH":
            self.invalid = True
            self.last_error = ""
        elif await self.interface.read_u32(self.save_ptr + 0xde8) != await self.interface.read_u32(self.AP_HEADER_LOCATION + 0x8):
            self.error("The loaded save file was created for a different multiworld. Choose a different save file.")

    async def validate_seed(self) -> None:
        if not self.server_connected or not self.slot_data:
            self.invalid = True
        # elif await self.interface.read_u32(self.AP_HEADER_LOCATION + 0x8) != self.slot_data["seed"]:
        #     self.error("The patch was created for a different multiworld. Make sure you are using the right patch and connecting to the correct multiworld.")

    async def server_auth(self, password_requested: bool = False) -> None:
        self.authenticating = True
        if password_requested and not self.password:
            await super(OoT3DClientContext, self).server_auth(password_requested)
        while not self.auth and not self.exit_event.is_set():
            await asyncio.sleep(1)
        await self.send_connect()
        self.authenticating = False
    
    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.server_connected = True

        if cmd == "LocationInfo":
            self.to_hint = [loc.location for loc in args["locations"]
                if loc.flags & (ItemClassification.progression | ItemClassification.useful)]
        
    async def get_pointers(self) -> bool:
        self.event_flags_ptr = await self.interface.read_u32(self.EVENTS_LOCATION)
        self.course_flags_ptr = await self.interface.read_u32(self.COURSES_LOCATION)
        self.minigame_ptr = await self.interface.read_u32(self.MINIGAME_LOCATION)
        if self.event_flags_ptr == 0 or self.course_flags_ptr == 0 or self.minigame_ptr == 0:
            return False
        return True

    async def is_in_game(self) -> bool:
        framework = await self.interface.read_u32(self.AP_HEADER_LOCATION + 0x54)
        if framework == 0:
            return False
        task_mgr = await self.interface.read_u32(framework + 0x1c)
        start_node = task_mgr + 0x44
        node = await self.interface.read_u32(start_node + 4)
        loop_count = 0
        while node != start_node and loop_count < 100:
            task = await self.interface.read_u32(node + 8)
            task_vtable = await self.interface.read_u32(task)
            if task_vtable == self.TASK_MAIN_GAME_VTABLE:
                return True
            node = await self.interface.read_u32(node + 4)
            loop_count += 1
        return False

    async def read_flags(self) -> None:
        cur_event_flags = await self.interface.read(self.event_flags_ptr + 0x48, 0x80)
        save_event_flags = await self.interface.read(self.save_ptr + 0x40, 0x80)
        self.event_flags = bytes_or(cur_event_flags, save_event_flags)

        cur_minigame_flags = (await self.interface.read(self.minigame_ptr + 0x35, 1))[0]
        save_minigame_flags = (await self.interface.read(self.save_ptr + 0xda5, 1))[0]
        self.minigame_flags = cur_minigame_flags | save_minigame_flags

        for course in range(0, 0x20):
            cur_course_flags = (await self.interface.read(self.course_flags_ptr + course * 0x16c + 0x160, 0x20)) \
                             + (await self.interface.read(self.course_flags_ptr + course * 0x16c + 0x1a0, 0x10))
            save_course_flags = await self.interface.read(self.save_ptr + 0x560 + course * 0x40, 0x40)
            self.course_flags.append(bytes_or(cur_course_flags, save_course_flags))

    def check_flag(self, course: Optional[int], flag: int) -> bool:
        byte = flag >> 3
        mask = 1 << (flag & 7)
        if course is None:
            return self.event_flags[byte] & mask != 0
        else:
            return self.course_flags[course][byte] & mask != 0

    # def check_location(self, loc: LocationData):
    #     return False

    async def check_locations(self) -> None:
        pass

    async def get_item(self) -> None:
        pass
    
    async def get_null_item(self) -> None:
        pass

async def game_watcher(ctx: OoT3DClientContext) -> None:
    global citra
    global triple
    global triple_addr
    ctx.interface = citra
    while not ctx.exit_event.is_set():
        try:
            ctx.invalid = False
            if not ctx.interface_connected:
                if triple_addr != "":
                    if await triple.connect(triple_addr):
                        if ctx.show_triple_connected_message:
                            logger.info("3ds connected!")
                        ctx.initial_delay = True
                        ctx.interface = triple
                        ctx.interface_connected = True
                        ctx.show_citra_connect_message = False
                        ctx.show_triple_connected_message = False
                    else:
                        logger.info("Couldn't connect to 3ds.")
                        ctx.interface_connected = False
                        triple.disconnect()
                        triple_addr = ""
                else:
                    triple.disconnect()
                    ctx.interface_connected = False
                    ctx.show_triple_connected_message = True
                    ctx.interface = citra
                    await ctx.citra_connect()
            else:
                if ctx.initial_delay:
                    delay = 1
                    if ctx.interface == triple:
                        delay = 5
                    await asyncio.sleep(delay)
                    ctx.initial_delay = False
                await ctx.validate_rom()
                if not ctx.invalid:
                    await ctx.validate_seed()
                if not ctx.invalid:
                    if await ctx.is_in_game():
                        await ctx.validate_save()
                        if triple_addr == "" and ctx.interface == triple:
                            ctx.interface_connected = False
                            triple.disconnect()
                        if not ctx.invalid and ctx.server_connected and (await ctx.get_pointers()):
                            await ctx.check_locations()
                            await ctx.get_item()
                        else:
                            ctx.initial_delay = True
                    else:
                        await ctx.get_null_item()
        except CitraException as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            ctx.interface_connected = False
            ctx.last_error = ""
            ctx.show_citra_connect_message = True
        except TripleException as e:
            if str(e) != "":
                logger.error(e)
                logger.error(traceback.format_exc())
            ctx.interface_connected = False
            ctx.last_error = ""
            ctx.show_citra_connect_message = True
            ctx.interface = citra
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            await ctx.disconnect()
            ctx.interface_connected = False
            ctx.server_connected = False
            ctx.last_error = ""
            ctx.show_citra_connect_message = True
        await asyncio.sleep(0.25)

def launch_client(*launch_args) -> None:
    async def main():
        parser = get_base_parser()
        args = parser.parse_args(launch_args)

        ctx = OoT3DClientContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.error("".join(traceback.format_exception(e)))

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()