import requests
import json

def return_search_results(query):
    # replace spaces with pluses for url
    query_plusses = query.replace(" ", "+")
    headers = {'Accept': 'application/json'}
    url = (
        f"https://www.curseforge.com/api/v1/mods/search"
        f"?gameId=432&index=0&classId=4471"
        f"&filterText={query_plusses}"
        f"&pageSize=20&sortField=2"
    )

    try:
        # send request
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()  # return parsed json
    except Exception as e:
        print(f"error fetching search results: {e}")
        return None

def get_files_list(id):
  headers = {'Accept': 'application/json'}
  url = (
      f"https://www.curseforge.com/api/v1/mods/{id}/files"
  )

  try:
      # send request
      resp = requests.get(url, headers=headers)
      resp.raise_for_status()
      return resp.json()  # return parsed json
  except Exception as e:
      print(f"error fetching files list: {e}")
      return None

def main():
    query = "all the mods 10"
    results = return_search_results(query)
    if not results or 'data' not in results:
        print("no data returned")
        return

    mods = results['data']
    if not mods:
        print("no mods found")
        return

    # list mods with index
    for i, mod in enumerate(mods):
        print(f"[{i}] {mod['name']} [{mod['id']}]")

    # prompt user
    choice = input("select index: ")
    try:
        idx = int(choice)
        # ensure valid range
        if idx < 0 or idx >= len(mods):
            raise IndexError
        selected_id = mods[idx]['id']
        print(selected_id)
        print(get_files_list(selected_id))
    except (ValueError, IndexError):
        print("invalid selection")

if __name__ == "__main__":
    main()
