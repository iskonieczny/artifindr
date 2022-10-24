import { useEffect, useState } from 'react';
import { kratos } from '../kratos/kratos';
import { config } from '../kratos/config';
import { useRouter } from '../hooks/useRouter';

export default function LoginPage() {
  const [flow, setFlow] = useState(null);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const router = useRouter()
  const {
    return_to: returnTo,
    flow: flowId,
    // Refresh means we want to refresh the session. This is needed, for example, when we want to update the password
    // of a user.
    refresh,
    // AAL = Authorization Assurance Level. This implies that we want to upgrade the AAL, meaning that we want
    // to perform two-factor authentication/verification.
    aal,
  } = router.query

  const initRedirect = () => {
    window.location.href = config.routes.login.selfServiceUrl;
  };

  useEffect(() => {
    // If the router is not ready yet, or we already have a flow, do nothing.
    if (!flowId) {
      initRedirect()
    }

    // If ?flow=.. was in the URL, we fetch it
    if (flowId) {
      kratos
        .getSelfServiceLoginFlow(String(flowId))
        .then(({data}) => {
          setFlow(data)
        })
        .catch(() => initRedirect())
      return
    }

    // Otherwise we initialize it
    kratos
      .initializeSelfServiceLoginFlowForBrowsers(
        Boolean(refresh),
        aal ? String(aal) : undefined,
        returnTo ? String(returnTo) : undefined,
      )
      .then(({ data }) => {
        setFlow(data)
      })
      .catch(() => initRedirect())
  }, [])
  console.log(flow)

  return (
    <div>
      <h1>Loginxd</h1>

      {flow?.ui?.messages && (
        <pre style={{ color: 'red' }}>{JSON.stringify(flow.ui.messages, null, 2)}</pre>
      )}

      <pre>{JSON.stringify({ action: flow?.ui?.action }, null, 2)}</pre>

      <pre>
        {JSON.stringify(
          {
            email,
            password,
            // @ts-ignore
            csrf_token:
              flow?.ui?.nodes?.find(n => n.attributes.name === 'csrf_token')?.attributes?.value || null,
          },
          null,
          2
        )}
      </pre>

      {flow && flow?.ui?.action && (
        <form
          id='login'
          method='post'
          action={flow.ui.action}
          encType='application/x-www-form-urlencoded'
          style={{ display: 'grid', gap: '1rem', maxWidth: 400 }}
        >
          <input
            id='csrf_token'
            name='csrf_token'
            type='hidden'
            required
            readOnly
            // @ts-ignore
            defaultValue={flow.ui.nodes.find(n => n.attributes.name === 'csrf_token')?.attributes.value}
          />

          <label htmlFor='traits.email'>
            <input
              type='email'
              id='traits.email'
              name='traits.email'
              placeholder='Email'
              value={email}
              onChange={({ target }) => {
                setEmail(target.value);
              }}
            />
          </label>

          <label htmlFor='password'>
            <input
              type='password'
              id='password'
              name='password'
              placeholder='Password'
              value={password}
              onChange={({ target }) => {
                setPassword(target.value);
              }}
            />
          </label>
          <button form='registration' formAction={flow.ui.action} formMethod='post' type='submit'>
            LOGIN
          </button>
          <button type="submit" name="provider" value="google">
              Login with github
          </button>
        </form>
      )}
    </div>
  );
}
