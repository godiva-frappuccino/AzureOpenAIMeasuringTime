import openai
import time
import statistics
from enum import Enum

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"

QUERY_FIRST = "Hello. answer in 1 word."
USER_QUERY = "Please tell me about Azure OpenAI Service."
SUFFIX_SHORT = "Answer in 1 sentence."
SUFFIX_LONG = "Answer in 10 sentences."

OUTPUT_RESPONSE_MESSAGE = False

ENDPOINT_JP = "<Insert Japan East URL>"
ENDPOINT_US = "<Insert East US URL>"
KEY_JP = "<Insert Japan East Key>"
KEY_US = "<Insert East US Key>"

class Region(Enum):
    Jp = 1
    Us = 2

def set_api(region : Region) -> None:
    if region == Region.Jp:
        openai.api_base = ENDPOINT_JP
        openai.api_key = KEY_JP
    elif region == Region.Us:
        openai.api_base = ENDPOINT_US
        openai.api_key = KEY_US

def first_request() -> None:
    messages = [
        {"role": "user", "content": QUERY_FIRST}
    ]
    response = openai.ChatCompletion.create(
        engine="gpt35",
        messages=messages,
    )

def request(is_stream : bool, is_long : bool) -> float:
    messages = [
        {"role": "user", "content": (USER_QUERY + SUFFIX_LONG) if is_long else (USER_QUERY + SUFFIX_SHORT)}
    ]
    start = time.time()
    response = openai.ChatCompletion.create(
        engine="gpt35",
        messages=messages,
        temperature=0,
        stream=is_stream
    )
    first = start # initialize
    if is_stream:
        for i, chunk in enumerate(response):
            if i == 0:
                first = time.time()
            if len(chunk["choices"]) >= 1:
                next = chunk["choices"][0]["delta"].get("content", "")
                if OUTPUT_RESPONSE_MESSAGE:
                    print(next, end="")
        print("")
    else:
        if OUTPUT_RESPONSE_MESSAGE:
            print(response["choices"][0]["message"]["content"])                
    end = time.time()
    return (end - start), (first - start)
    
def trial(region : Region, is_stream : bool, is_long : bool) -> None:
    set_api(region)
    print("REGION:{0}, STREAMING:{1}, LONG:{2}".format(region, is_stream, is_long))
    result_last = []
    result_first = []
    first_request()
    for i in range(10):
        print("Test {0}:".format(i))
        last, first = request(is_stream, is_long)
        result_last.append(last)
        result_first.append(first)
    # use only last when trial is not stream condition.
    print("First mean:{0}, stdev:{1}".format(statistics.mean(result_first), statistics.stdev(result_first)))
    print("Last mean:{0}, stdev:{1}".format(statistics.mean(result_last), statistics.stdev(result_last)))

def main() -> None:
    trial(Region.Jp, False, False)
    trial(Region.Jp, False, True)
    trial(Region.Jp, True, True)
    # if response is not long, it's no need streaming response
    trial(Region.Us, False, False)
    trial(Region.Us, False, True)
    trial(Region.Us, True, True)
    # if response is not long, it's no need streaming response

if __name__ == "__main__":
    main()