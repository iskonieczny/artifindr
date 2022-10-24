const publicUrl = 'http://127.0.0.1:4433/';
const adminUrl = 'http://127.0.0.1:4434/';
const browserUrl = 'http://127.0.0.1:4433/';

export const config = {
  kratos: {
    publicUrl,
    adminUrl,
    browserUrl,
  },

  routes: {
    registration: {
      path: '/auth/registration',
      selfServiceUrl: `${publicUrl}/self-service/registration/browser`,
    },
    login: {
      path: '/auth/login',
      selfServiceUrl: `${publicUrl}/self-service/login/browser`,
    },
    verify: {
      path: '/auth/verify',
      selfServiceUrl: `${publicUrl}/self-service/verify/browser`,
    },
    recovery: {
      path: '/auth/recovery',
      selfServiceUrl: `${publicUrl}/self-service/recovery/browser`,
    },
    settings: {
      path: '/auth/login',
      selfServiceUrl: `${publicUrl}/self-service/settings/browser`,
    },
    dashboard: {
      path: '/dashboard',
    },
  },

  labels: {
    to_verify: {
      label: 'Email',
      priority: 100,
    },
    csrf_token: {
      label: '',
      priority: 100,
    },
    'traits.email': {
      label: 'Email',
      priority: 90,
    },
    email: {
      label: 'Email',
      priority: 80,
    },
    identifier: {
      label: 'Email',
      priority: 80,
    },
    password: {
      label: 'Password',
      priority: 80,
    },
    'traits.name.first': {
      label: 'First name',
      priority: 95,
    },
    'traits.name.last': {
      label: 'Last name',
      priority: 96,
    },
  },
};
