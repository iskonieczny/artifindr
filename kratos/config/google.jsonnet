local claims = {
  email_verified: true
} + std.extVar('claims');

{
  identity: {
    traits: {
      email: claims.email,
			first_name: claims.given_name,
			last_name: claims.family_name,
    },
  },
}