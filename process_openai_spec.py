import requests
import yaml
import os

def fetch_openai_spec(url, output_filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"Content successfully fetched from {url} and saved to {output_filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return False
    except IOError as e:
        print(f"Error saving file: {e}")
        return False

def parse_openai_paths(input_filename, output_directory):
    try:
        with open(input_filename, "r") as f:
            openapi_spec = yaml.safe_load(f)

        if "paths" not in openapi_spec:
            print(f"Error: 'paths' section not found in {input_filename}")
        else:
            paths = openapi_spec["paths"]

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
                print(f"Created directory: {output_directory}")

            for path, content in paths.items():
                filename = path.replace("/", "_")
                if filename.startswith("_"):
                    filename = filename[1:]
                output_filepath = os.path.join(output_directory, f"{filename}.yaml")

                with open(output_filepath, "w") as f:
                    yaml.dump({path: content}, f, indent=2)
                print(f"Saved path '{path}' to {output_filepath}")
        return True
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found. Please ensure it exists.")
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def extract_schemas(input_filename, output_directory):
    try:
        with open(input_filename, "r") as f:
            openapi_spec = yaml.safe_load(f)

        if "components" not in openapi_spec or "schemas" not in openapi_spec["components"]:
            print(f"Error: 'components/schemas' section not found in {input_filename}")
        else:
            schemas = openapi_spec["components"]["schemas"]

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
                print(f"Created directory: {output_directory}")

            for schema_name, schema_content in schemas.items():
                output_filepath = os.path.join(output_directory, f"{schema_name}.yaml")
                with open(output_filepath, "w") as f:
                    yaml.dump({schema_name: schema_content}, f, indent=2)
                print(f"Saved schema '{schema_name}' to {output_filepath}")
        return True
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found. Please ensure it exists.")
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def extract_groups(input_filename, output_base_directory):
    try:
        with open(input_filename, "r") as f:
            openapi_spec = yaml.safe_load(f)

        if "x-oaiMeta" not in openapi_spec:
            print(f"Error: 'x-oaiMeta' section not found in {input_filename}")
        elif "navigationGroups" not in openapi_spec["x-oaiMeta"]:
            print(f"Error: 'x-oaiMeta/navigationGroups' section not found in {input_filename}")
        elif "groups" not in openapi_spec["x-oaiMeta"]:
            print(f"Error: 'x-oaiMeta/groups' section not found in {input_filename}")
        else:
            navigation_groups = openapi_spec["x-oaiMeta"]["navigationGroups"]
            groups = openapi_spec["x-oaiMeta"]["groups"]

            if not os.path.exists(output_base_directory):
                os.makedirs(output_base_directory)
                print(f"Created directory: {output_base_directory}")

            for nav_group in navigation_groups:
                nav_group_id = nav_group["id"]
                nav_group_path = os.path.join(output_base_directory, nav_group_id)
                if not os.path.exists(nav_group_path):
                    os.makedirs(nav_group_path)
                    print(f"Created navigation group directory: {nav_group_path}")

            for group in groups:
                group_id = group["id"]
                navigation_group_id = group.get("navigationGroup")

                if navigation_group_id:
                    output_directory = os.path.join(output_base_directory, navigation_group_id)
                    output_filepath = os.path.join(output_directory, f"{group_id}.yaml")
                    with open(output_filepath, "w") as f:
                        yaml.dump(group, f, indent=2)
                    print(f"Saved group '{group_id}' to {output_filepath}")
                else:
                    print(f"Warning: Group '{group_id}' has no 'navigationGroup' specified. Skipping.")
        return True
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found. Please ensure it exists.")
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    OPENAPI_URL = "https://raw.githubusercontent.com/openai/openai-openapi/refs/heads/manual_spec/openapi.yaml"
    OPENAPI_FILENAME = "openai-api-spec.yaml"
    PATHS_DIR = "paths"
    SCHEMAS_DIR = "schemas"
    GROUPS_DIR = "groups"

    if fetch_openai_spec(OPENAPI_URL, OPENAPI_FILENAME):
        print("\n--- Processing Paths ---")
        parse_openai_paths(OPENAPI_FILENAME, PATHS_DIR)

        print("\n--- Extracting Schemas ---")
        extract_schemas(OPENAPI_FILENAME, SCHEMAS_DIR)

        print("\n--- Extracting Groups ---")
        extract_groups(OPENAPI_FILENAME, GROUPS_DIR)

    print("\nNote: If you encounter a 'ModuleNotFoundError: No module named 'yaml'' or 'requests' error, please install them using: pip install PyYAML requests")