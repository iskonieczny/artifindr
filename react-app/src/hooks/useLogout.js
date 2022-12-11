import { AxiosError } from "axios"
import { useRouter } from "./useRouter"
import { useState, useEffect, DependencyList } from "react"

import {kratos} from "../kratos/kratos"

// Returns a function which will log the user out
export function useLogout(deps=[]) {  
  const [logoutToken, setLogoutToken] = useState("")
  const router = useRouter()

  useEffect(() => {
    kratos
      .createSelfServiceLogoutFlowUrlForBrowsers()
      .then(({ data }) => {
        setLogoutToken(data.logout_token)
      })
      .catch((err) => {
        switch (err.response?.status) {
          case 401:
            // do nothing, the user is not logged in
            return
        }

        // Something else happened!
        return Promise.reject(err)
      })
  }, deps)

  return () => {
    if (logoutToken) {
      kratos
        .submitSelfServiceLogoutFlow(logoutToken)
        .then(() => window.location.href = '/')
    }
  }
}
