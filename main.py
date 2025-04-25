import requests
import json
import os
from urllib.parse import quote


def build_download_url(file_id: int, file_name: str) -> str:
    # forge cdn pattern -> files/<id//1000>/<id%1000 padded>/<encoded filename>
    dir1 = file_id // 1000
    dir2 = f"{file_id % 1000:03d}"
    encoded = quote(file_name)
    return f"https://mediafilez.forgecdn.net/files/{dir1}/{dir2}/{encoded}"


def download_file(file_id: int, file_name: str, dest_folder: str = "..") -> None:
    # stream download to disk
    url = build_download_url(file_id, file_name)
    # THIS IS THE KEY CHANGE: os.path.join("..", file_name) will resolve correctly
    path = os.path.join(dest_folder, file_name)

    print(f"downloading {file_name} -> {path}") # Path will now show the parent directory
    print(f"cdn url: {url}")

    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(path, "wb") as fh:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        fh.write(chunk)
        print("download complete\nyou can now remove the directory this script is in")
    except Exception as e:
        print(f"error downloading file: {e}")


def return_search_results(query: str) -> dict | None:
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


def get_files_list(project_id: int) -> dict | None:
    url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files"
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching files list: {e}")
        return None


def get_additional_files(project_id: int, file_id: int) -> dict | None:
    url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/additional-files"
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching additional files: {e}")
        return None


def choose_from_list(items, label_key, id_key):
    for idx, itm in enumerate(items):
        print(f"[{idx}] {itm[label_key]} [{itm[id_key]}]")
    choice = input("select index: ")
    try:
        i = int(choice)
        if 0 <= i < len(items):
            return items[i]
    except ValueError:
        pass
    print("invalid selection")
    return None


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

    file_id     = chosen_file["id"]
    file_name   = chosen_file["fileName"]

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
            download_file(chosen_sp["id"], chosen_sp["fileName"])
            return

    # default: download normal client zip
    download_file(file_id, file_name)

if __name__ == "__main__":
    main()
