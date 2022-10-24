import {
  SelfServiceRegistrationFlow,
  SubmitSelfServiceRegistrationFlowBody,
} from "@ory/client"
import { useRouter } from "../hooks/useRouter"
import { useEffect, useState } from "react"
import { config } from "../kratos/config"
import { getFormFieldTitle, getFormPlaceholder, filterFields } from "../kratos/translations"

// Import the SDK
import { kratos } from "../kratos/kratos"

// Renders the registration page
const Register = () => {
  const router = useRouter()

  // The "flow" represents a registration process and contains
  // information about the form we need to render (e.g. username + password)
  const [flow, setFlow] = useState()

  // Get ?flow=... from the URL
  const { flow: flowId, return_to: returnTo } = router.query

  const initRedirect = () => {
    window.location.href = config.routes.registration.selfServiceUrl;
  };

  // In this effect we either initiate a new registration flow, or we fetch an existing registration flow.
  useEffect(() => {
    
    // If the router is not ready yet, or we already have a flow, do nothing.

    // If ?flow=.. was in the URL, we fetch it
    if (flowId) {
      
      kratos
        .getSelfServiceRegistrationFlow(String(flowId))
        .then(({ data }) => {
          // We received the flow - let's use its data and render the form!
          setFlow(data)
        })
        .catch(err => console.log(err))
      return
    }

    // Otherwise we initialize it
    initRedirect()
  }, [])

  console.log(flow)

  const onSubmit = (values) =>
    router
      // On submission, add the flow ID to the URL but do not navigate. This prevents the user loosing
      // his data when she/he reloads the page.
      .navigate(`/auth/register?flow=${flow?.id}`, undefined, { shallow: true })
      .then(() =>
        kratos
          .submitSelfServiceRegistrationFlow(String(flow?.id), values)
          .then(({ data }) => {
            // If we ended up here, it means we are successfully signed up!
            //
            // You can do cool stuff here, like having access to the identity which just signed up:
            console.log("This is the user session: ", data, data.identity)

            // For now however we just want to redirect home!
            return router.navigate(flow?.return_to || "/").then(() => {})
          })
          .catch(err => console.log(err))
          .catch((err) => {
            // If the previous handler did not catch the error it's most likely a form validation error
            if (err.response?.status === 400) {
              // Yup, it is!
              console.log(err.response?.data)
              setFlow(err.response?.data)
              return
            }

            return Promise.reject(err)
          }),
      )

    console.log(flow)

  return flow?.ui?.nodes && (
    <>
      <form
        action={flow.ui.action}
        method={flow.ui.method}
        onSubmit={onSubmit}
      >
        {flow.ui.messages?.map(el => <>{el.text}</>)}
        {flow.ui.nodes.map((field, index) => <div
          className={`form-group ${field.attributes.type !== "hidden" ? "visible" : "d-none"}`}
        >
          <label htmlFor={field.name} className="form-label">
            {getFormFieldTitle(field.attributes)}
          </label>
          <input
            className="form-control"
            defaultValue={field.attributes.value}
            disabled={field.attributes.disabled}
            id={field.attributes.name}
            name={field.attributes.name}
            pattern={field.attributes.pattern}
            placeholder={getFormPlaceholder(field.attributes)}
            required={field.attributes.required}
          />
        </div>)}
        <button type="submit">Submit</button>
      </form>
    </>
  )
}

export default Register