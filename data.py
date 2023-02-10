ACCOUNT_PAYLOAD = {
    "viewVersion": "v1",
    "viewTimeRange": {"viewTimeRangeType": "LAST_7"},
    "viewType": "CUSTOMER",
    "viewVisualization": {
        "groupBy": {
            "fieldId": "awsServiceCode",
            "fieldName": "Service",
            "identifier": "AWS",
            "identifierName": "AWS",
        },
        "chartType": "STACKED_TIME_SERIES",
    },
    "name": "Perspective-<AWSAccountName>",
    "viewRules": [
        {
            "viewConditions": [
                {
                    "type": "VIEW_ID_CONDITION",
                    "viewField": {
                        "fieldId": "awsUsageAccountId",
                        "fieldName": "Account",
                        "identifier": "AWS",
                    },
                    "viewOperator": "IN",
                    "values": ["<AWSAccountName> (<AWS Account ID>)"],
                }
            ]
        }
    ],
    "viewState": "COMPLETED",
    "viewPreferences": {"includeOthers": False, "includeUnallocatedCost": False},
    "folderId": "tSqskO0LSkC3wfK9cwvasd",
}

APPLICATION_PAYLOAD = {
    "viewVersion": "v1",
    "viewTimeRange": {"viewTimeRangeType": "LAST_7"},
    "viewType": "CUSTOMER",
    "viewVisualization": {
        "groupBy": {
            "fieldId": "awsServiceCode",
            "fieldName": "Service",
            "identifier": "AWS",
            "identifierName": "AWS",
        },
        "chartType": "STACKED_TIME_SERIES",
    },
    "name": "Perspective-<appName>",
    "viewRules": [
        {
            "viewConditions": [
                {
                    "type": "VIEW_ID_CONDITION",
                    "viewField": {
                        "fieldId": "labels.value",
                        "fieldName": "user_chewy_app_name",
                        "identifier": "LABEL",
                    },
                    "viewOperator": "IN",
                    "values": ["<appName>"],
                }
            ]
        }
    ],
    "viewState": "COMPLETED",
    "viewPreferences": {"includeOthers": False, "includeUnallocatedCost": False},
    "folderId": "tSqskO0LSkC3wfK9cwvasd",
}

PERSPECTIVES_PAYLOAD = {
    "query": """query FetchAllPerspectives($folderId: String, $sortCriteria: QLCEViewSortCriteriaInput = null) {
        perspectives(folderId: $folderId, sortCriteria: $sortCriteria) {
            sampleViews {
                id
                name
                chartType
                createdAt
                viewState
                lastUpdatedAt
                __typename
            }
            customerViews {
                id
                name
                chartType
                totalCost
                viewType
                viewState
                createdAt
                lastUpdatedAt
                timeRange
                reportScheduledConfigured
                dataSources
                folderId
                folderName
                groupBy {
                    fieldId
                    fieldName
                    identifier
                    identifierName
                    __typename
                }
                __typename
            }
            __typename
        }
    }""",
    "operationName": "FetchAllPerspectives",
    "variables": {"folderId": "tSqskO0LSkC3wfK9cwvasd"},
}

BUDGET_PAYLOAD = {
    "accountId": "8M1tvFxMTW-FW2EC3uywQg",
    "name": "<Budget Name>",
    "alertThresholds": [
        {
            "basedOn": "ACTUAL_COST",
            "emailAddresses": ["<Enter the EmailID List>"],
            "percentage": 100,
            "userGroupIds": [],
            "slackWebhooks": [],
        }
    ],
    "type": "PREVIOUS_PERIOD_SPEND",
    "period": "YEARLY",
    "startTime": 1669766400000,
    "growthRate": 0,
    "budgetAmount": 34639439.69,
    "scope": {
        "viewName": "<Perspective Name>",
        "type": "PERSPECTIVE",
        "viewId": "<Perspective ID>",
    },
    "budgetMonthlyBreakdown": {
        "budgetBreakdown": "MONTHLY",
        "budgetMonthlyAmount": [],
    },
}
