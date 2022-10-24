import { useEffect, useState } from 'react';
import { kratos } from '../kratos/kratos';
import { config } from '../kratos/config';
import { useRouter } from '../hooks/useRouter';

export default function LoginPage() {
  const [flowResponse, setFlowResponse] = useState(null);

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

  useEffect(() => {

    const initRedirect = () => {
      window.location.href = config.routes.login.selfServiceUrl;
    };

    console.log('[LOGIN] flowId: ', flowId);

    if (!flowId) {
      initRedirect();
    }

    if (flowId) {
      kratos
        .getSelfServiceLoginFlow(document.cookie, flowId).then((flow) => {
          console.log('[LOGIN] flow: ', flow);

          if ([403, 404, 410].includes(flow.status)) {
            console.log('[LOGIN] status = 403 | 404 | 410: ', flow.status);
            //initRedirect();
          }

          if (flow.status !== 200) {
            console.log('[LOGIN] status !== 200: ', flow);
            //initRedirect();
          }

          setFlowResponse(flow.data);
          console.log('[LOGIN] flow success: ', flow);
        })
        .catch(err => {
          console.error('[LOGIN] err: ', err);
          //initRedirect();
        });
    }
  }, []);

  return (
    <div>
      <h1>Login</h1>

      {flowResponse?.ui?.messages && (
        <pre style={{ color: 'red' }}>{JSON.stringify(flowResponse.ui.messages, null, 2)}</pre>
      )}

      <pre>{JSON.stringify({ action: flowResponse?.ui?.action }, null, 2)}</pre>

      <pre>
        {JSON.stringify(
          {
            email,
            password,
            // @ts-ignore
            csrf_token:
              flowResponse?.ui?.nodes?.find(n => n.attributes.name === 'csrf_token')?.attributes?.value || null,
          },
          null,
          2
        )}
      </pre>

      {flowResponse && flowResponse?.ui?.action && (
        <form
          id='login'
          method='post'
          action={flowResponse.ui.action}
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
            defaultValue={flowResponse.ui.nodes.find(n => n.attributes.name === 'csrf_token')?.attributes.value}
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
          <button form='registration' formAction={flowResponse.ui.action} formMethod='post' type='submit'>
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
