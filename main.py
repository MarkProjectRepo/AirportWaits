import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def pull_webpage(url: str) -> str:
    return requests.get(url).content

def retrieve_wait_times(request_content: str) -> pd.DataFrame:
    soup = BeautifulSoup(request_content, 'html.parser')
    data = {"Checkpoint":[],"Wait Time":[]}

    table = soup.find("table", attrs = {"class":"views-table" })
    body = table.find("tbody")
    rows = body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        (c,w) = [ele.text.strip() for ele in cols if ele.text.strip()]
        data["Checkpoint"] += [c]
        data["Wait Time"] += [w]

    data = pd.DataFrame(data)
    return data

def index_by_datetime(df: pd.DataFrame, outdir: str = "./data/") -> None:
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    current_date = datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    path = path = os.path.join(outdir, "YYZ.csv")

    new_df = pd.DataFrame({a:[b] for _, (a,b) in df.iterrows()})
    new_df.index = pd.DatetimeIndex(data=[datetime.now()])

    if os.path.exists(path):
        out_df = pd.read_csv(path, index_col=0)
        out_df = pd.concat([out_df,new_df])
    else:
        out_df = new_df
    
    out_df.to_csv(path)


if __name__ == "__main__":
    url = "https://www.catsa-acsta.gc.ca/en/airport/toronto-pearson-international-airport"
    webpage = pull_webpage(url)
    df = retrieve_wait_times(webpage)
    index_by_datetime(df)
    