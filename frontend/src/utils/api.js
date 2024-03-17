export const callApi = async (url, token, callback) => {
  fetch(
    url,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      }
    }
  ).then((res) => {
    if (res.ok){
      res.json().then((data) => {
        callback(data);
      })
    } else {
      console.log('ERROR')
    }
  })
}
