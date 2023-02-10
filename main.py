from logging import error
from os import getenv
from datetime import datetime, timedelta

from requests import get, post, exceptions

from data import (
    ACCOUNT_PAYLOAD,
    APPLICATION_PAYLOAD,
    PERSPECTIVES_PAYLOAD,
    BUDGET_PAYLOAD,
)

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "x-api-key": getenv("HARNESS_PLATFORM_API_KEY"),
}

PARAMS = {
    "routingId": getenv("HARNESS_ACCOUNT_ID"),
    "accountIdentifier": getenv("HARNESS_ACCOUNT_ID"),
}


def get_start_time() -> int:
    """
    Get the time we should start a budget
    From Rohit, should be start of the last day of the previous month
    Returns: epoc time in milliseconds
    """

    today = datetime.now(tz=datetime.timezone.utc)

    first = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    last_day_last_month = first - timedelta(days=1)

    return int(last_month.timestamp()) * 1000


def create_account_perspective(name: str, aid: str) -> str:
    """
    Corrilate costs within an aws account
    Returns: link to the perspective
    """

    payload = ACCOUNT_PAYLOAD.copy()

    payload["name"] = "Perspective-" + name
    payload["viewRules"][0]["viewConditions"][0]["values"][0] = f"{name} ({aid})"
    payload["folderId"] = getenv("HARNESS_CCM_FOLDER")

    resp = post(
        "https://app.harness.io/gateway/ccm/api/perspective",
        headers=HEADERS,
        params=PARAMS,
        json=payload,
    )

    try:
        resp.raise_for_status()
    except Exception as e:
        try:
            data = resp.json()
        except exceptions.JSONDecodeError as f:
            raise e
        else:
            error(data["message"] + ": " + payload["name"])
            return ""

    data = resp.json()

    if data.get("status", "") == "SUCCESS":
        return f"https://app.harness.io/ng/#/account/{data['data']['accountId']}/ce/perspectives/{data['data']['uuid']}/name/{data['data']['name']}"
    else:
        return str(data)


def create_application_perspective(name: str) -> str:
    """
    Corrilate costs within an application
    Returns: link to the perspective
    """

    payload = APPLICATION_PAYLOAD.copy()

    payload["name"] = "Perspective-" + name
    payload["viewRules"][0]["viewConditions"][0]["values"][0] = name
    payload["folderId"] = getenv("HARNESS_CCM_FOLDER")

    resp = post(
        "https://app.harness.io/gateway/ccm/api/perspective",
        headers=HEADERS,
        params=PARAMS,
        json=payload,
    )

    try:
        resp.raise_for_status()
    except Exception as e:
        try:
            data = resp.json()
        except exceptions.JSONDecodeError as f:
            raise e
        else:
            error(data["message"] + ": " + payload["name"])
            return ""

    data = resp.json()

    if data.get("status", "") == "SUCCESS":
        return f"https://app.harness.io/ng/#/account/{data['data']['accountId']}/ce/perspectives/{data['data']['uuid']}/name/{data['data']['name']}"
    else:
        return str(data)


def get_perspectives() -> list:
    """
    Get all the perspectives in an account
    Returns: list of perspective objects
    """

    payload = PERSPECTIVES_PAYLOAD.copy()

    payload["variables"]["folderId"] = getenv("HARNESS_CCM_FOLDER")

    resp = post(
        "https://app.harness.io/gateway/ccm/api/graphql",
        headers=HEADERS,
        params=PARAMS,
        json=payload,
    )

    resp.raise_for_status()

    data = resp.json()

    return data.get("data", {}).get("perspectives", {}).get("customerViews", [])


def get_monthly_cost(perspective: str) -> dict:
    """
    Get all the perspectives in an account
    Returns: data on previous years cost by month
    """

    resp = post(
        "https://app.harness.io/gateway/ccm/api/perspective/lastYearMonthlyCost",
        headers=HEADERS,
        params=PARAMS.update(
            {
                "perspectiveId": perspective,
                "period": "YEARLY",
                "startTime": "1669766400000",
                "type": "PREVIOUS_PERIOD_SPEND",
                "breakdown": "MONTHLY",
            }
        ),
    )

    resp.raise_for_status()

    data = resp.json()

    return data


def create_budget(pname: str, pid: str) -> dict:
    """
    Create a budget based on a perspectives previous yearly spend
    Returns: response from harness
    """

    payload = BUDGET_PAYLOAD.copy()

    monthly_costs = get_monthly_cost(pid).get("data")

    if not monthly_costs:
        error("Unable to get cost data for " + pname)
        return

    year_cost = 0
    for m in monthly_costs:
        year_cost += m["value"]

    payload["accountId"] = getenv("HARNESS_ACCOUNT_ID")
    payload["name"] = pname + "-Budget"
    payload["alertThresholds"][0]["emailAddresses"] = []
    payload["budgetAmount"] = round(year_cost, 2)
    payload["startTime"] = get_start_time()
    payload["scope"]["viewName"] = pname
    payload["scope"]["viewId"] = pid
    payload["budgetMonthlyBreakdown"]["budgetMonthlyAmount"] = monthly_costs

    resp = post(
        "https://app.harness.io/gateway/ccm/api/budgets",
        headers=HEADERS.update({"authority": "app.harness.io"}),
        params=PARAMS,
        json=payload,
    )

    resp.raise_for_status()

    data = resp.json()

    return data


if __name__ == "__main__":

    print("something")

    # existing = get_perspectives()

    # name = input("Enter an account name\n")
    # aid = input("Enter an account id\n")

    # print(create_account_perspective(name, aid))

    # aname = input("Enter an application name\n")

    # print(create_application_perspective(aname))

    # for perspective in get_perspectives():
    # print(perspective)
    # costs = get_monthly_cost(perspective.get("id")).get("data", [])
