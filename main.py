from bs4 import BeautifulSoup
import requests
import csv

def get_so_jobs(term):
  job_list = []
  url = f"https://stackoverflow.com/jobs?r=true&q={term}"
  html_doc = requests.get(url).text
  soup = BeautifulSoup(html_doc, "html.parser")
  list_results = soup.find("div", {"class":"listResults"})
  head_soup = list_results.find_all("h2", {"class":"mb4 fc-black-800 fs-body3"})
  for head in head_soup:
    header = head.find("a")
    link = "https://stackoverflow.com" + header.get("href")
    title = header.get_text()
    job_list.append([title, "company_name", link])
  comp_soup = list_results.find_all("h3", {"class":"fc-black-700 fs-body1 mb4"})
  for i, company in enumerate(comp_soup):
    comp_name = company.find("span").text.strip()
    job_list[i][1] = comp_name

  return job_list


def get_wwr_jobs(term):
  job_list = []
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  html_doc = requests.get(url).text
  soup = BeautifulSoup(html_doc, "html.parser")
  list_soup = soup.find("ul")
  list_item = list_soup.find_all("li", {"class":"feature"})
  for info in list_item:
    title = info.find("span", {"class":"title"}).text
    company = info.find("span", {"class":"company"}).text
    link = "https://weworkremotely.com" + info.find("a").get("href")
    job_list.append([title, company, link])
  
  return job_list


def get_remo_jobs(term):
  job_list = []
  url = f"https://remoteok.io/remote-dev+{term}-jobs"
  html_doc = requests.get(url).text
  soup = BeautifulSoup(html_doc, "html.parser")
  tr_soup = soup.find_all("tr", {"class":"job"})
  for tr in tr_soup:
    title = tr.find("h2", {"itemprop":"title"}).text
    company = tr.get("data-company")
    link = "https://remoteok.io" + tr.get("data-href")
    job_list.append([title, company, link])

  return job_list

term = input("Enter the job title: ")
csv_output = False
while True:
  csv_output = {"csv": True, "xlsx": False}.get(input("Enter the output file type (csv/xlsx): ").lower())
  if csv_output is not None:
    break
  print("Invalid output file type!")
job_list = get_so_jobs(term) + get_wwr_jobs(term) + get_remo_jobs(term)
jobs_df = pd.DataFrame(job_list, columns=["title", "company", "url"])
if csv_output:
  jobs_df.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
else:
  jobs_df.to_excel("jobs.xlsx",  index=False)
print(f"Found {len(joblist)} jobs.")
