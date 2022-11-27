import { useRouter } from "../hooks/useRouter"
import { useEffect, useState } from "react"
import { getFormFieldTitle, getFormPlaceholder, filterFields } from "../kratos/translations"
import { handleFlowError } from "../kratos/errors"
import { useSelector, useDispatch } from 'react-redux'
import { setFlow } from "../ducks/actions"
import { kratos } from "../kratos/kratos"
import { useVerify } from "../hooks/useVerify"

const Login = () => {
  const router = useRouter()
  const flow = useSelector((state) => state.flow)
  const dispatch = useDispatch()
  const sendVerify = useVerify()
  const [values, setValues] = useState({})

  const initializeValues = (nodes = []) => {
    console.log(nodes)
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
  const resetFlow = (value) => {dispatch(setFlow(value))}

  useEffect(() => {
    if (flowId) {
      kratos
        .getSelfServiceLoginFlow(String(flowId))
        .then(({ data }) => {
          dispatch(setFlow(data))
          initializeValues(data.ui.nodes)
        })
        .catch(handleFlowError(router, "login", resetFlow))
      return
    }
    kratos
      .initializeSelfServiceLoginFlowForBrowsers(
        returnTo ? String(returnTo) : undefined,
      )
      .then(({ data }) => {
        dispatch(setFlow(data))
        initializeValues(data.ui.nodes)
      })
      .catch(e => console.log(e))
  }, [])

  const onSubmit = (e) => {
    e.stopPropagation()
    e.preventDefault()
    console.log(values)
    kratos
      .submitSelfServiceLoginFlow(String(flow?.id), values)
      .then(({ data }) => {
        console.log("This is the user session: ", data, data.identity)
        return router.navigate(flow?.return_to || "/")
      })
      .catch(handleFlowError(router, "login", resetFlow))
      .catch((err) => {
        if (err.response?.status === 400) {
          console.log(err.response?.data)
          dispatch(setFlow(err.response?.data))
          return
        }

        return Promise.reject(err)
      })
    }

  const isNotActive = flow?.ui?.messages?.[0].id === 4000010

  return flow?.ui?.nodes && (
    <div className="d-flex justify-content-center flex-wrap">
      <div className="m-3 p-3 rounded-5 bg-semi-light">
        <div className="cred-input text-red">{flow.ui.messages?.map(el => <>{el.text}</>)}</div>
        {
          isNotActive && 
          <button onClick={() => sendVerify(values["identifier"])}>
            Resend activation link
          </button>
        }
        <form
          action={flow.ui.action}
          method={flow.ui.method}
          onSubmit={onSubmit}
        >
          {filterFields(flow.ui.nodes).map((field, index) => <div
            className={`form-group ${field.attributes.type !== "hidden" ? "visible" : "d-none"}`}
          >
            <label htmlFor={field.name} className="form-label">
              {getFormFieldTitle(field.attributes)}
            </label>
            <input
              className="form-control cred-input align-items-center"
              defaultValue={field.attributes.value}
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
              <span className="cred-input text-red" key={`${id}-${k}`} data-testid={`ui/message/${id}`}>
                {text}
              </span>
            ))}
          </>
          </div>)}
          <button type="submit" className='mt-2 p-2 btn btn-primary rounded-5 btn-lg'>Submit</button>
        </form>
        
      </div>
      <div className="align-self-start m-3 p-3 rounded-5 bg-semi-light">
      <form
          action={flow.ui.action}
          method={flow.ui.method}
        >
          <button type="submit" name="provider" value="google" className="p-2 btn btn-primary rounded-5 btn-lg">
            Log in with Google
          </button>
            </form>
      </div>
    </div>
  )
}

export default Login