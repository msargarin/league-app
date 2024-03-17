import { Button, Card, Label, Select } from "flowbite-react";
import { useRef } from "react";

const LoginPage = function ({ setUser }) {
  const roleSelect = useRef();
  const handleLogin = async (e) => {
    e.preventDefault();

    // Request for access token based on selected role
    await fetch("http://localhost:8000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ role: roleSelect.current.value }),
    }).then((res) => {
      if (res.ok) {
        res.json().then((data) => {
          // Set user to 'authenticated' user
          setUser({
            name: data.name,
            team: data.team,
            role: data.role,
            token: data.access_token,
          });
        });
      }
    });
  };

  return (
    <div className="flex flex-col items-center justify-center px-6 lg:h-screen lg:gap-y-12">
      <div className="my-6 flex items-center gap-x-1 lg:my-0">
        <img
          alt="Flowbite logo"
          src="https://flowbite.com/docs/images/logo.svg"
          className="mr-3 h-12"
        />
        <span className="self-center whitespace-nowrap text-2xl font-semibold dark:text-white">
          League App
        </span>
      </div>
      <Card
        horizontal
        className="w-full md:max-w-screen-sm [&>img]:hidden md:[&>img]:w-96 md:[&>img]:p-0 md:[&>*]:w-full md:[&>*]:p-16 lg:[&>img]:block"
      >
        <form onSubmit={(e) => handleLogin(e)}>
          <div className="mb-4 flex flex-col gap-y-3">
            <Label htmlFor="role">
              <h1 className="mb-3 text-2xl font-bold dark:text-white md:text-3xl">
                Choose your role
              </h1>
            </Label>
            <Select id="role" ref={roleSelect} required>
              <option value="admin">Admin</option>
              <option value="coach">Coach</option>
              <option value="player">Player</option>
            </Select>
          </div>
          <div className="mb-6">
            <Button type="submit" className="w-full">
              Login
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default LoginPage;
