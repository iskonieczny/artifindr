import { useRouter } from "../hooks/useRouter"
import { useEffect, useState } from "react"
import { getFormFieldTitle, getFormPlaceholder, filterFields } from "../kratos/translations"
import { handleFlowError } from "../kratos/errors"
import { useSelector, useDispatch } from 'react-redux'
import { setFlow } from "../ducks/actions"
import { kratos } from "../kratos/kratos"

const Register = () => {
  const router = useRouter()
  const flow = useSelector((state) => state.flow)
  const dispatch = useDispatch()
  const [values, setValues] = useState({})

  const initializeValues = (nodes = []) => {
    nodes.forEach((node) => {
        if (
          node.attributes.type === "button" ||
          node.attributes.name === "provider"
        ) {
          return
        }
        values[node.attributes.name] = node.attributes.value
      }
    )
    setValues( values )
  }

  const { flow: flowId, return_to: returnTo } = router.query

  useEffect(() => {
    if (flowId) {
      kratos
        .getSelfServiceRegistrationFlow(String(flowId))
        .then(({ data }) => {
          dispatch(setFlow(data))
          initializeValues(data.ui.nodes)
        })
        .catch(handleFlowError(router, "registration", resetFlow))
      return
    }
    kratos
      .initializeSelfServiceRegistrationFlowForBrowsers(
        returnTo ? String(returnTo) : undefined,
      )
      .then(({ data }) => {
        dispatch(setFlow(data))
        initializeValues(data.ui.nodes)
      })
      .catch(e => console.log(e))
  }, [])

  const resetFlow = (value) => {dispatch(setFlow(value))}

  const onSubmit = (e) => {
    e.stopPropagation()
    e.preventDefault()
    kratos
      .submitSelfServiceRegistrationFlow(String(flow?.id), values)
      .then(({ data }) => {
        console.log("This is the user session: ", data, data.identity)
        return router.navigate(flow?.return_to || "/")
      })
      .catch(handleFlowError(router, "registration", resetFlow))
      .catch((err) => {
        if (err.response?.status === 400) {
          console.log(err.response?.data)
          dispatch(setFlow(err.response?.data))
          return
        }

        return Promise.reject(err)
      })
    }

  return flow?.ui?.nodes && (
    <>
      <form
        action={flow.ui.action}
        method={flow.ui.method}
        onSubmit={onSubmit}
      >
        {flow.ui.messages?.map(el => <>{el.text}</>)}
        {filterFields(flow.ui.nodes).map((field, idx) => 
        <div key={idx} className={`form-group ${field.attributes.type !== "hidden" ? "visible" : "d-none"}`}>
          <label htmlFor={field.name} className="form-label">
            {getFormFieldTitle(field.attributes)}
          </label>
          <input
            className="form-control"
            //defaultValue={field.attributes.value}
            type={field.attributes.type}
            value={values[field.attributes.name] || field.attributes.value || ''}
            onChange={e => setValues({...values, [field.attributes.name]: e.target.value})}
            disabled={field.attributes.disabled}
            id={field.attributes.name}
            name={field.attributes.name}
            pattern={field.attributes.pattern}
            placeholder={getFormPlaceholder(field.attributes)}
            required={field.attributes.required}
          />
          <>
          {field.messages.map(({ text, id }, k) => (
            <span key={`${id}-${k}`} data-testid={`ui/message/${id}`}>
              {text}
            </span>
          ))}
        </>
        </div>)}
        <button type="submit">Submit</button>
      </form>
    </>
  )
}

export default Register