import {
  SelfServiceVerificationFlow,
  SubmitSelfServiceVerificationFlowBody,
} from "@ory/client"
import { useRouter } from "../hooks/useRouter"
import { useEffect, useState } from "react"
import {kratos} from "../kratos/kratos"
import { config } from "../kratos/config"
import { getFormFieldTitle, getFormPlaceholder, filterFields } from "../kratos/translations"

const Verify = () => {
  const [flow, setFlow] = useState()

  // Get ?flow=... from the URL
  const router = useRouter()
  const { flow: flowId, return_to: returnTo } = router.query

  const initRedirect = () => {
    window.location.href = config.routes.verify.selfServiceUrl;
  };

  useEffect(() => {
    // If the router is not ready yet, or we already have a flow, do nothing.

    // If ?flow=.. was in the URL, we fetch it
    if (flowId) {
      kratos
        .getSelfServiceVerificationFlow(String(flowId))
        .then(({ data }) => {
          setFlow(data)
        })
        .catch((err) => {
          switch (err.response?.status) {
            case 410:
            // Status code 410 means the request has expired - so let's load a fresh flow!
            case 403:
              // Status code 403 implies some other issue (e.g. CSRF) - let's reload!
              return router.push("/auth/verify")
          }

          throw err
        })
      return
    }

    // Otherwise we initialize it
    initRedirect()
  }, [])

  const onSubmit = (values) =>
    router
      // On submission, add the flow ID to the URL but do not navigate. This prevents the user loosing
      // his data when she/he reloads the page.
      .push(`auth/verify?flow=${flow?.id}`, undefined, { shallow: true })
      .then(() =>
        kratos
          .submitSelfServiceVerificationFlow(
            String(flow?.id),
            values,
            undefined,
          )
          .then(({ data }) => {
            // Form submission was successful, show the message to the user!
            setFlow(data)
          })
          .catch((err) => {
            switch (err.response?.status) {
              case 400:
                // Status code 400 implies the form validation had an error
                setFlow(err.response?.data)
                return
            }

            throw err
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

export default Verify