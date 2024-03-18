import { useState } from "react";
import { Alert } from "flowbite-react";
import { HiInformationCircle } from "react-icons/hi";
import LoginForm from "./pages/LoginPage";
import AppNavbar from "./components/AppNavbar";
import HomePage from "./pages/HomePage";
import TeamPage from "./pages/TeamPage";

import { BrowserRouter } from "react-router-dom";
import { Routes, Route, Outlet } from "react-router";
import PlayerPage from "./pages/PlayerPage";

function App() {
  const [user, setUser] = useState(null);

  return user ? (
    <BrowserRouter>
      <Routes>
        <Route
          element={
            <>
              <AppNavbar user={user} setUser={setUser} />

              <div className="flex items-start">
                <main className="relative h-full w-full overflow-y-auto bg-gray-100 dark:bg-gray-900">
                  <Alert
                    color="success"
                    icon={HiInformationCircle}
                    className="m-4"
                  >
                    <h3 className="text-lg">
                      You are logged in as&nbsp;
                      {user.role == "admin" ? (
                        <b>the league admin</b>
                      ) : (
                        <>
                          a <b className="uppercase">{user.role}</b> of&nbsp;
                          <b className="uppercase">{user.team}</b>
                        </>
                      )}
                    </h3>
                  </Alert>

                  <div className="block items-center justify-between border-b border-gray-200 bg-white p-4 m-4 dark:border-gray-700 dark:bg-gray-800 sm:flex rounded-lg shadow">
                    <Outlet />
                  </div>
                </main>
              </div>
            </>
          }
        >
          <Route
            path="/"
            element={<HomePage user={user} setUser={setUser} />}
            index
          />
          <Route
            path="/team/:teamId"
            element={<TeamPage user={user} setUser={setUser} />}
          />
          <Route
            path="/player/:playerId"
            element={<PlayerPage user={user} setUser={setUser} />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  ) : (
    <LoginForm setUser={setUser} />
  );
}

export default App;
