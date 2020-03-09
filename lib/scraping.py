import lxml.html
import requests

def get_issues():
    base_url = "https://github.com/brokenManager"
    r = requests.get(base_url)
    html = lxml.html.fromstring(r.text)
    elems = html.xpath('//*[@id="org-repositories"]/div[1]/div/ul/li')
    repos = []
    for elem in elems:
        e = elem.xpath("div[1]/div[1]/h3/a")[0].text
        repos.append(e.strip())
    results = []
    for repo in repos:
        repo_url = base_url + "/{}/issues".format(repo)
        r = requests.get(repo_url)
        html = lxml.html.fromstring(r.text)
        repo_elems = html.xpath(
            '//*[@id="js-repo-pjax-container"]/div[2]/div/div/div[3]/div[2]/div/div'
        )
        for repo_elem in repo_elems:
            results.append(
                {
                    "repo": repo,
                    "id"  : repo_elem.attrib["id"][6:]
                }
            )
    return results


if __name__ == "__main__":
    issues = get_issues()
    print(issues)

