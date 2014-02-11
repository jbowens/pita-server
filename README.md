My Little PITA Server
=====================

The server for My Little PITA. This server does not provide
any frontend for the website.

### Authentication

Some endpoints require account authentication. For these endpoints, the server expects two
custom headers to be sent with the request.

- `X-PITA-ACCOUNT-ID` - the account id of the account to authenticate as
- `X-PITA-SECRET` - the secret key associated with the account

### Endpoints

A list of currently provided endpoints.

#### POST /accounts/new

Creates a new account.

- `name` *(required)* -- the name associated with the account. It does not need to be unique.
- `phone` -- the phone number associated with the account. If provided, it must be unique.
- `email` -- the email address associated with the account. If provided, it must be unique.

Either the phone number or email must be present. On success, the endpoint returns a JSON payload
of the following form.

```json
{
    "aid": 105,
    "key": "2SW0X5JCNG2BHDO7ASUYYX36S9LDUOJ0MOGR5IKRH714GFJU6FYER2T4X4LZYW68IC6K17A2ZKS2KP83AIQYSJB9MWVVWVRXXSXADUZR92JC3YYF1VNTJXJ71LA1GMN7"
}
```

The `aid` is the id of the created account. The `key` is a secret 128 character hash. It is used for authentication on
any endpoints that require user authentication.

#### POST /error

Records an error that occurred on the client. This can be used for discovering/gaining debug data
about bugs on the client.

- `message` *(required)* -- a message describing the error condition that occurred.

On success, the endpoint returns a JSON payload of the following form.

```json
{"status": "ok"}
```

