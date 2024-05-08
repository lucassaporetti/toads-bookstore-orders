import logging
import httpx

from bookstore_orders.components.utils.exceptions import ToadsBookstoreOrdersException

logger = logging.getLogger()


def _get_headers(id_account=None):
    headers = dict()
    headers["Content-Type"] = "application/json"
    headers['id-account'] = str(id_account)
    return headers


async def send_api_request(req, headers=None, id_account=None):
    endpoint = req.endpoint
    method = (
        req._method  # pylint: disable=protected-access
        if hasattr(req, "_method")
        else "post"
    )

    logger.info(f"Sending a {method} request to: {endpoint}")

    request_data = req.dict(by_alias=True, exclude_none=True)

    logger.info(f"Request body/params: {request_data}")

    if not headers:
        headers = _get_headers(id_account=id_account)

    logger.info(f"Request HEADERS: {headers}")

    async with httpx.AsyncClient() as client:
        try:
            if method == "get":
                res = await client.get(url=endpoint, params=request_data, headers=headers, timeout=100)
            elif method == "put":
                res = await client.put(url=endpoint, json=request_data, headers=headers, timeout=100)
            elif method == "patch":
                res = await client.patch(url=endpoint, json=request_data, headers=headers, timeout=100)
            else:
                res = await client.post(url=endpoint, json=request_data, headers=headers, timeout=100)
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"integration_request_error | request_method: {method} | "
                f"request_url: {endpoint!r} | request_body: {request_data} | "
                f"response_code: {exc.response.status_code} | response_body {exc.response.text}"
            )
            raise ToadsBookstoreOrdersException(
                exc.response.status_code,
                exc.response.text,
            ) from exc

        logger.info(
            f"integration_request_success | request_method: {method} | "
            f"request_url: {endpoint!r} | request_body: {request_data} | "
            f"response_code: {res.status_code} | response_body {res.text}"
        )
        return res.json()
