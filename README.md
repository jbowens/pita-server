My Little PITA Server
=====================

The server for My Little PITA. This server does not provide
any frontend for the website.

## Authentication

Some endpoints require account authentication. For these endpoints, the server expects two
custom headers to be sent with the request.

- `X-PITA-ACCOUNT-ID` - the account id of the account to authenticate as
- `X-PITA-SECRET` - the secret key associated with the account

## HTTP Endpoints

A list of currently provided http endpoints.

### /accounts endpoints

##### POST /accounts/new

Creates a new account.

- `uuid` *(required)* -- device specific uuid. It must be unique.
- `name`  -- the name associated with the account. It does not need to be unique.
- `phone` -- the phone number associated with the account. If provided, it must be unique.
- `email` -- the email address associated with the account. If provided, it must be unique.

On success, the endpoint returns a JSON payload of the following form.

```json
{
    "aid": 105,
    "key": "2SW0X5JCNG2BHDO7ASUYYX36S9LDUOJ0MOGR5IKRH714GFJU6FYER2T4X4LZYW68IC6K17A2ZKS2KP83AIQYSJB9MWVVWVRXXSXADUZR92JC3YYF1VNTJXJ71LA1GMN7"
}
```

The `aid` is the id of the created account. The `key` is a secret 128 character hash. It is used for authentication on
any endpoints that require user authentication.

##### POST /accounts/location

Records an account location. This endpoint requires account authentication.

- `latitude` *(required)* -- the latitude of the account"s location
- `longitude` *(required)* -- the longitude of the account"s location
- `time` -- when the account was at the given location

If no `time` is provided, the current time is assumed. On success, returns
```json
{"status": "ok"}
```

##### POST /accounts/nearby

Requests information about other nearby accounts. This endpoint requires
account authentication. Optionally, the current latitude and longitude
may be sent along with the request.

- `latitude` -- the latitude of the account's current location
- `longitude` -- the longitude of the account's current location

On success, the result has the following form:

```json
{
    "nearby_accounts": [
        {
            "aid": 5936
        },
        {
            "aid": 6036,
            "pita_name": "Optimistic Cruelty"
        }
    ]
}
```

Accounts without a pita name do not yet have a Pita.

### /pitas endpoints

##### POST /pitas/random

Creates a random pita for the authorized account. This endpoint requires account authentication.
No parameters are necessary. The endpoint returns a serialized Pita. Only one pita may exist for
each account.

```json
{
    "pid": 25525,
    "aid": 2952,
    "state": "egg",
    "parent_a": null,
    "parent_b": null,
    "body_hue": 2.6336,
    "spots_hue": 0.212,
    "tail_hue": 5.422,
    "has_spots": true
}
```

##### POST /pitas/save

Saves a Pita's state attributes. This endpoint requires account authentication. It will
update the current primary pita for the account.

- `happiness` *(required)* -- the current happiness value of the pita
- `hunger` *(required)* -- the current hunger value of the pita
- `sleepiness` *(required)* -- the current sleepiness value of the pita

A standard status json payload is sent in return:

```json
{"status": "ok"}
```

##### POST /pitas/get

Retrieves a Pita. This endpoint requires account authentication. The json
payload contains all data pertaining to the Pita. This includes static data
like visual properties as well as state attributes. If there is no pita
associated with the current account, the following is returned:

```json
{"status": "ok", "has_pita": false}
```

Otherwise, a standard serialized pita is returned.

##### POST /pitas/hatch

Records a Pita's hatching. This endpoint requires account authentication.
A standard success json payload is returned when successful.

```json
{"status": "ok"}
```

##### POST /pitas/death

Records a Pita's death. This endpoint requires account authentication.
A standard success json payload is returned when successful.

```json
{"status": "ok"}
```

##### POST /pitas/disown

Records that a Pita has been disowned by its owner. This endpoint requires
account authentication. A standard success json payload is returned when
successful.

```json
{"status": "ok"}
```

### / endpoints

##### POST /error

Records an error that occurred on the client. This can be used for discovering/gaining debug data
about bugs on the client.

- `message` *(required)* -- a message describing the error condition that occurred.

On success, the endpoint returns a JSON payload of the following form.

```json
{"status": "ok"}
```

### /photos endpoints

##### POST /photos/record

Records a photo that was taken on the client. We can use the photos retrieved through this endpoint
for improving our computer vision algorithm. This endpoint requires account authentication.

- `photo` *(required)* -- image payload
- `context` -- a description of the context in which the photo was taken, for ex. feeding, etc.

This endpoint uses Amazon S3 for storing the image.

