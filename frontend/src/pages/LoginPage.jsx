import { Button, Card, Label, Select } from "flowbite-react";
import { GiBasketballBall } from "react-icons/gi";

import { useRef } from "react";
import { getAcessToken } from "../utils/api";

const LoginPage = function ({ setUser }) {
  const roleSelect = useRef();
  const handleLogin = async (e) => {
    e.preventDefault();

    // Request for access token based on selected role
    getAcessToken(roleSelect.current.value, setUser);
  };

  return (
    <div className="flex flex-col items-center justify-center px-6 lg:h-screen lg:gap-y-12">
      <div className="my-6 flex items-center gap-x-1  lg:my-0">
        <GiBasketballBall className="text-5xl mr-1 text-teal-600 dark:text-teal-200" />
        <h1 className="self-center whitespace-nowrap text-5xl font-semibold dark:text-white text-teal-900">
          League App
        </h1>
      </div>
      <Card
        horizontal
        className="w-full md:max-w-screen-sm [&>img]:hidden md:[&>img]:w-96 md:[&>img]:p-0 md:[&>*]:w-full md:[&>*]:p-16 lg:[&>img]:block"
      >
        <form onSubmit={(e) => handleLogin(e)}>
          <div className="mb-4 flex flex-col gap-y-3">
            <Label htmlFor="role">
              <h2 className="mb-3 text-xl font-semibold dark:text-white md:text-3xl">
                Choose your role
              </h2>
            </Label>
            <Select id="role" ref={roleSelect} required>
              <option value="admin">Admin</option>
              <option value="coach">Coach</option>
              <option value="player">Player</option>
            </Select>
          </div>
          <div className="mb-6">
            <Button type="submit" className="w-full">
              LOGIN
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default LoginPage;
