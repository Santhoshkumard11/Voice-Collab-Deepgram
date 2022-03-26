import os

DOMAIN_NAME = os.getenv("DOMAIN_NAME")

COMMAND_DETAILS: dict = {
    1: {
        "method_name": "trigger_pipeline_run",
        "description": "Triggering Azure DevOps pipeline ",
    },
    2: {
        "method_name": "execute_on_shell",
        "args": ["pip freeze > requirements.txt"],
        "kargs": {},
        "success_message": "Successfully created requirements file",
        "failure_message": "Failed to create requirements file",
    },
    3: {
        "method_name": "get_total_pipeline_runs",
        "description": "Triggering Azure DevOps pipeline ",
    },
    4: {"method_name": "initiate_teams_call", "description": "call some on teams"},
    5: {"method_name": "initiate_a_mail", "description": "mail some on teams"},
    6: {"method_name": "open_teams_chat", "description": "call some on teams"},
    7: {"method_name": "initiate_teams_call", "description": "call some on teams"},
}

COMMAND_MAPPINGS: dict = {
    1: ["start build", "trigger build pipeline"],
    2: ["create requirements.txt", "create requirements"],
    3: [],
    4: [],
    5: [],
}

# Microsoft Accounts
MSFT_ACCOUNT_NAME_LIST: list = [
    {
        "name": "Alex",
        "id": "329420-2384932-234832-24324",
        "email": f"AlexW{DOMAIN_NAME}",
    },
    {
        "name": "Grady",
        "id": "4985739-485692-958749-6847989",
        "email": f"GradyA{DOMAIN_NAME}",
    },
    {
        "name": "Megan",
        "id": "84898795-238779-9457-459964",
        "email": f"MeganB{DOMAIN_NAME}",
    },
]


def add_msft_account_to_commands():

    # adding members to the mapping list
    for account in MSFT_ACCOUNT_NAME_LIST:
        name = account.get("name")

        COMMAND_MAPPINGS.get(3).append(f"call {name}")
        COMMAND_MAPPINGS.get(4).append(f"mail {name}")
        COMMAND_MAPPINGS.get(5).append(f"open {name}'s chat")


add_msft_account_to_commands()