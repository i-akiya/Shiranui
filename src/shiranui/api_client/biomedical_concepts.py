import requests


class BiomedicalConcepts:

    @classmethod
    def get_bc_list_from_api_v2(cls, api_key: str) -> list:
        """
        Class method to get a list of biomedical concepts v2 from the CDISC Library API

        Args:
            api_key_str (str): API key string for authentication

        Returns:
            response: The HTTP response object containing the biomedical concept data

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """
        headers = {
            "api-key": api_key,
            "aaccept": "application/json"
        }

        try:
            url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return [response.json().get("_links").get("biomedicalConcepts")]

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error

    @classmethod
    def get_latest_bc_cat_from_api_v2(cls, api_key: str) -> list:
        """
        Class method to get a list of latest biomedical concepts categories v2 from the CDISC Library API

        Args:
            api_key (str): API key string for authentication

        Returns:
            response: The HTTP response object containing the biomedical concept category data

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """

        try:
            url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/categories"

            headers = {
                "api-key": api_key,
                "aaccept": "application/json"
            }

            response = requests.get(url, headers=headers)

            return [response.json().get("_links").get("categories")]

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error


    @classmethod
    def get_latest_bc_from_api_v2(cls, api_key: str, concept_id: str) -> dict:
        """
        Class method to get detailed information for a specific biomedical concept v2 from the CDISC Library API

        Args:
            api_key (str): API key string for authentication
            concept_id (str): The ID of the biomedical concept to retrieve

        Returns:
            response: The HTTP response object containing detailed information about the specified biomedical concept

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """

        try:
            url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts/{concept_id}"

            headers = {
                "api-key": api_key,
                "aaccept": "application/json"
            }

            response = requests.get(url, headers=headers)

            return response.json()

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error


    @classmethod
    def get_bc_package_list_from_api_v2(cls, api_key: str) -> list:
        """
        Class method to get a list of biomedical concept packages from the CDISC Library API Biomedical Concepts V2.

        Args:
            api_key (str): API key string for authentication

        Returns:
            response: The HTTP response object containing the biomedical concept package data

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """

        headers = {
            "api-key": api_key,
            "accept": "application/json"
        }

        try:
            url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return [response.json().get("_links").get("packages")]

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error


    @classmethod
    def get_bc_for_package_from_api_v2(cls, api_key: str,
        package_id: str,
        biomedicalconcept_id: str) -> dict:
        """
        Class method to get detailed information for a specific biomedical concept package from the CDISC Library API Biomedical Concepts V2.

        Args:
            api_key (str): API key string for authentication
            package_id (str): The ID of the package containing the biomedical concept
            biomedicalconcept_id (str): The ID of the biomedical concept to retrieve

        Returns:
            response: The HTTP response object containing detailed information about the specified biomedical concept within a package

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """

        try:
            url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package_id}/biomedicalconcepts/{biomedicalconcept_id}"

            headers = {
                "api-key": api_key,
                "accept": "application/json"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error


    @classmethod
    def get_bc_package_from_api_v2(cls, api_key: str,
        package_id: str) -> list:
        """
        Class method to get a list of biomedical concepts for a specific package from the CDISC Library API Biomedical Concepts V2.

        Args:
            api_key (str): API key string for authentication
            package_id (str): The ID of the package containing the biomedical concepts

        Returns:
            response: The HTTP response object containing the list of biomedical concepts within the specified package

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code
            requests.exceptions.ConnectionError: If a network problem occurred
            requests.exceptions.Timeout: If the request timed out
            requests.exceptions.RequestException: For any other request-related error
        """

        try:
            url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package_id}/biomedicalconcepts"

            headers = {
                "api-key": api_key,
                "accept": "application/json"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return [response.json().get("_links").get("biomedicalConcepts")]

        except requests.exceptions.HTTPError as error_http:
            raise error_http
        except requests.exceptions.ConnectionError as error_connection:
            raise error_connection
        except requests.exceptions.Timeout as time_out_error:
            raise time_out_error
        except requests.exceptions.RequestException as other_error:
            raise other_error
