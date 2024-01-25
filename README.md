# ico2-api
Proof of concept api for ico2

Entites :

Scope :

```json
    {
        "id": 1,
        "label": "Dep - Environement"
    }
```

Category :

```json
    {
        "id": 1,
        "label": "Staff",
    },
```

Unit :

```json
    {
        "id": 1,
        "label": "Litre",
        "symb": "L"
    }
```

Item :

```json
    {
        "id": 1,
        "label": "Local Francais",
        "categoryId": 1,
        "scopeId": 1,
        "isActive": true,
    }
```

Factor :

```json
    {
    "id" : 1,
    "valeur": 13,
    "unitId": 1,

    "source" : "Interne",
    "sourceLabel": "",
    "sourceIdentifier": null,
    "isActive": true
    }
```

Routes :

/api/scopes
=> Return the list of all scopes

```json
    [
        {
            "id": 1,
            "label": "Dep - Environement"
        },
        ...
    ]
```

/api/categories
=> Return the list of all categorires

```json
    [
        {
            "id": 1,
            "label": "Staff",
        },
        ...
    ]
```

/api/items/lookup?category=1&scope=1
=> Return the list of all items filtered by categoryId, scopeId AND return all the actives items

```json
    [
        {
            "id": 1,
            "label": "Local Francais",
        },
        ...
    ]
```

/api/items/1/factors
=> Return the list of all facotors for a given item (1) resolt the unitId to a unit object

```json
    [
        {
            "id" : 1,
            "valeur": 13,
            "unit": {
                "id": 1,
                "label": "Litre",
                "symb": "L"
            }
        },
        ...
    ]
```

Imports:

```json
{
    "label": "Diesel",
    "categoryLabel": "Transport",
    "scopeLabel": "Commun",
    "factors": [
        {
            "value": 3.15,
            "unit": {
                "label": "Litre",
                "symb": "L",
            },
        }
        ]
} 
```