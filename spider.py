import multiprocessing
import random
import string
import re
import requests
import bs4 as bs
import sys
import argparse

def random_starting_url():
    starting = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(3))
    url = "".join(["http://", starting, ".com"])
    return url

def handle_local_links(url, link):
    if link.startswith("/"):
        return "".join([url, link])
    return link

def get_links(url):
    try:
        response = requests.get(url, timeout=5)
        soup = bs.BeautifulSoup(response.text, "lxml")
        body = soup.body
        links = [link.get("href") for link in body.find_all("a")]
        links = [handle_local_links(url, link) for link in links]
        links = [str(link) for link in links]
        return links

    except TypeError as e:
        print(e)
        print("Got a type error, probably got a None that we tried to iterate over")
        return []
    except IndexError as e:
        print(e)
        print("we probably did not find any useful links, returning empty list")
        return []
    except AttributeError as e:
        print(e)
        print("likely got None for links, so we are throwing this")
        return []
    except Exception as e:
        print(str(e))
        return []
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
        return []
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
        return []
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
        return []
    except KeyboardInterrupt:
        print("Someone closed the program")

def emlgrb_by_url(url):
    try:
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, "lxml")
        emails = list(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.text, re.I))
        return emails
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL, requests.exceptions.ContentDecodingError, requests.exceptions.ChunkedEncodingError,
            requests.exceptions.TooManyRedirects) as e:
        print(e)
        return []
    except UnicodeError as e:
        print(e)
        return []


def spider():
        p = multiprocessing.Pool(processes=100)
        parse_us = [random_starting_url() for _ in range(100)]
        data = p.map(get_links, parse_us)
        data = sum(data, [])
        p.close()
        p.join()
        #emailss = emlgrb(data)  --> in case you use emlgrb function without multiprocessing
        px = multiprocessing.Pool(processes=100)
        emailss = px.map(emlgrb_by_url, data, chunksize=10)
        emailsss = set(sum(emailss, []))
        px.close()
        px.join()

        with open("emails_2.txt", "a") as f:
            f.write("\n" + "\n")
            f.write(str(emailsss))


if __name__ == "__main__":
    num = input("choose number of iteration: ")
    print("There are %d CPUs on this machine" % multiprocessing.cpu_count())
    for _ in range(int(num)):
        spider()
