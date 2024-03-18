export const callApi = async (url, user, setUser, callback, setUserHasAccess) => {
  await fetch(
    url,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${user.token.access}`,
      }
    }
  ).then((res) => {
    if (res.ok){
      res.json().then((data) => {
        // Handle data as needed
        callback(data);

        // Set access control if available
        if (setUserHasAccess) {
          // User has access to resourse
          setUserHasAccess(true);
        }
      })
    } else {
      // Handle 401 error
      if (res.status == 401){
        // Refresh our token
        getRefreshToken(user, setUser);
      } else if (res.status == 403){
        // Set access control if available
        if (setUserHasAccess) {
          // User has no access to resourse
          setUserHasAccess(false)
        }

        // Send back empty data
        callback({});
      } else {
        console.log('ERROR')
      }
    }
  })
}

export const getAcessToken = async (requested_role, setUser) => {
  await fetch("http://localhost:8000/token/access", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ role: requested_role }),
  }).then((res) => {
    if (res.ok) {
      res.json().then((data) => {
        // Set user to 'authenticated' user
        setUser({
          name: data.name,
          team: data.team,
          role: data.role,
          token: {
            access: data.access_token,
            refresh: data.refresh_token,
          },
        });
      });
    }
  });
}

export const getRefreshToken = async (user, setUser) => {
  await fetch("http://localhost:8000/token/refresh", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh: user.token.refresh }),
  }).then((res) => {
    if (res.ok) {
      res.json().then((data) => {
        // Set new tokens to user
        setUser({
          ...user,
          token: {
            access: data.access,
            refresh: data.refresh,
          },
        });
      });
    }
  });
}
