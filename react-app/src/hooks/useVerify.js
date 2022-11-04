import { AxiosError } from "axios"
import { useRouter } from "./useRouter"
import { useState, useEffect, DependencyList } from "react"
import {kratos} from "../kratos/kratos"

export function useVerify() {  
  const [flow, setFlow] = useState("")
  const [values, setValues] = useState({})

  const initializeValues = (nodes = []) => {
    console.log(nodes)
    nodes.forEach((node) => {
        values[node.attributes.name] = node.attributes.value
      }
    )
    setValues( values )
  }

  useEffect(() => {
    kratos
      .initializeSelfServiceVerificationFlowForBrowsers()
      .then(({ data }) => {
        setFlow(data)
        initializeValues(data.ui.nodes)
      })
      .catch((err) => {
        throw err
      })
  }, [])

  return (email) => {
    if (flow) {
      kratos
        .submitSelfServiceVerificationFlow(String(flow.id), {...values, email: email})
        .then(() => alert("Email has been sent!"))
        .catch((err) => {
          console.log(err.response?.data)
        })
    }
  }
}
