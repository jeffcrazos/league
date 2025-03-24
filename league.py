import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

seasons = [
    "2015–16", "2016–17", "2017–18", "2018–19", "2019–20",
    "2020–21", "2021–22", "2022–23", "2023–24"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"
}

all_matches = []

def parse_page(url, season, stage):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {season} ({stage}): {e}")
        return
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    
    tables = soup.find_all("table", class_="wikitable")
    
    current_date = "Unknown Date"  
    
    for table in tables:
        
        rows = table.find_all("tr")[1:]  
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:  
                date_elem = row.find_previous("span", class_="mw-headline")
                if date_elem and re.match(r"Matchday|Round|Quarter|Semi|Final", date_elem.get_text()):
                    current_date = date_elem.get_text(strip=True)
                elif row.find_previous("td", text=re.compile(r"\d{1,2}\s\w+\s\d{4}")):
                    date_text = row.find_previous("td", text=re.compile(r"\d{1,2}\s\w+\s\d{4}")).get_text(strip=True)
                    current_date = date_text if date_text else current_date
                
                match_info = cols[1].get_text(strip=True) if len(cols) > 1 else "N/A"
                if "–" in match_info or "-" in match_info:  
                    home_team = cols[0].get_text(strip=True)
                    away_team = cols[2].get_text(strip=True) if len(cols) > 2 else "N/A"
                    score = match_info
                    
                    
                    all_matches.append({
                        "Season": season,
                        "Stage": stage,
                        "Date": current_date,
                        "Home Team": home_team,
                        "Away Team": away_team,
                        "Score": score
                    })


for season in seasons:
    print(f"Парсинг сезона {season}...")
    
   
    group_stage_url = f"https://en.wikipedia.org/wiki/{season}_UEFA_Champions_League_group_stage"
    parse_page(group_stage_url, season, "Group Stage")
    
    
    knockout_url = f"https://en.wikipedia.org/wiki/{season}_UEFA_Champions_League_knockout_phase"
    parse_page(knockout_url, season, "Knockout Phase")


df = pd.DataFrame(all_matches)


df.drop_duplicates(inplace=True)
df.sort_values(by=["Season", "Date"], inplace=True)


output_file = "champions_league_2015_2024_full.csv"
df.to_csv(output_file, index=False)

print(f"Dataset сохранён в '{output_file}'")
print(f"Всего матчей: {len(df)}")
print(df.head()) 
