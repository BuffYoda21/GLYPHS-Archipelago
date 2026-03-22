from worlds.LauncherComponents import Component, Type, components, launch

def run_client(*args: str) -> None:
    from .client.client import launch_client
    launch(launch_client, name="OoT3D Client", args=args)

components.append(
    Component(
        "OoT3D Client",
        func=run_client,
        game_name="Ocarina of Time 3D",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
