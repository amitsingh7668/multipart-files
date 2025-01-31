wireMockServer.givenThat(post(urlEqualTo(TRADING_ACCOUNT_URL + VALID_CCONSOL))
        .withHeader("Content-Type", equalTo("application/json"))
        .withHeader("Authorization", matching("Bearer .*")) // Matches any Bearer token
        .withRequestBody(matchingJsonPath("$.name", equalTo("systemId"))) // Ensures JSON body has systemId
        .willReturn(aResponse()
                .withStatus(200)
                .withBody(aTradingAccountResponse)
                .withHeader("Content-Type", "application/json")));
