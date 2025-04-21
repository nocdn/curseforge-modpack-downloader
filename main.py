import requests
import json

# ---------------- search ----------------
def return_search_results(query: str) -> dict | None:
    # build search url
    url = (
        "https://www.curseforge.com/api/v1/mods/search"
        f"?gameId=432&index=0&classId=4471"
        f"&filterText={query.replace(' ', '+')}"
        "&pageSize=20&sortField=2"
    )
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching search results: {e}")
        return None


# ---------------- files list for a project ----------------
def get_files_list(project_id: int) -> dict | None:
    # fetch list of files for a modpack
    url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files"
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching files list: {e}")
        return None


# ---------------- additional files (server packs) ----------------
def get_additional_files(project_id: int, file_id: int) -> dict | None:
    # fetch server packs etc
    url = (
        f"https://www.curseforge.com/api/v1/mods/"
        f"{project_id}/files/{file_id}/additional-files"
    )
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching additional files: {e}")
        return None


# ---------------- pretty list helper ----------------
def choose_from_list(items, label_key, id_key):
    # print list and return chosen item or None
    for idx, item in enumerate(items):
        print(f"[{idx}] {item[label_key]} [{item[id_key]}]")
    choice = input("select index: ")
    try:
        i = int(choice)
        if 0 <= i < len(items):
            return items[i]
    except ValueError:
        pass
    print("invalid selection")
    return None


# ---------------- main flow ----------------
def main():
    query = input("search curseforge for: ")
    search_res = return_search_results(query)
    if not search_res or "data" not in search_res or not search_res["data"]:
        print("no results")
        return

    chosen_project = choose_from_list(search_res["data"], "name", "id")
    if not chosen_project:
        return

    project_id = chosen_project["id"]
    files_res = get_files_list(project_id)
    if not files_res or "data" not in files_res or not files_res["data"]:
        print("no files found")
        return

    chosen_file = choose_from_list(files_res["data"], "displayName", "id")
    if not chosen_file:
        return

    file_id = chosen_file["id"]
    if chosen_file.get("hasServerPack"):
        mode = input("download normal (n) or server pack (s)? ").lower().strip()
        if mode == "s":
            add_res = get_additional_files(project_id, file_id)
            if not add_res or "data" not in add_res or not add_res["data"]:
                print("no server packs found")
                return
            print("server files available:")
            chosen_sp = choose_from_list(add_res["data"], "displayName", "id")
            if not chosen_sp:
                return
            print(f"downloading server pack {chosen_sp['fileName']}")
            return

    # default normal download
    print(f"downloading {chosen_file['fileName']}")


if __name__ == "__main__":
    main()
