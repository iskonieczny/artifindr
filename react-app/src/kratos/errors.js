// A small function to help us deal with errors coming from fetching a flow.
export function handleGetFlowError(
  router,
  flowType,
  resetFlow
) {
  return async (err) => {
    switch (err.response?.data.error?.id) {
      case "session_aal2_required":
        // 2FA is enabled and enforced, but user did not perform 2fa yet!
        window.location.href = err.response?.data.redirect_browser_to
        return
      case "session_already_available":
        // User is already signed in, let's redirect them home!
        await router.navigate("/")
        return
      case "session_refresh_required":
        // We need to re-authenticate to perform this action
        window.location.href = err.response?.data.redirect_browser_to
        return
      case "self_service_flow_return_to_forbidden":
        // The flow expired, let's request a new one.
        alert("The return_to address is not allowed.")
        resetFlow(undefined)
        await router.navigate("/" + flowType)
        return
      case "self_service_flow_expired":
        // The flow expired, let's request a new one.
        alert("Your interaction expired, please fill out the form again.")
        resetFlow(undefined)
        await router.push("/" + flowType)
        return
      case "security_csrf_violation":
        // A CSRF violation occurred. Best to just refresh the flow!
        alert(
          "A security violation was detected, please fill out the form again.",
        )
        resetFlow(undefined)
        await router.push("/" + flowType)
        return
      case "security_identity_mismatch":
        // The requested item was intended for someone else. Let's request a new flow...
        resetFlow(undefined)
        await router.push("/" + flowType)
        return
      case "browser_location_change_required":
        // Ory Kratos asked us to point the user to this URL.
        window.location.href = err.response.data.redirect_browser_to
        return
    }

    switch (err.response?.status) {
      case 410:
        // The flow expired, let's request a new one.
        resetFlow(undefined)
        await router.navigate("/" + flowType)
        return
    }

    // We are not able to handle the error? Return it.
    return Promise.reject(err)
  }
}

// A small function to help us deal with errors coming from initializing a flow.
export const handleFlowError = handleGetFlowError
