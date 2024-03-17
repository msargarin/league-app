import { Breadcrumb, List } from "flowbite-react";
import { Link } from "react-router-dom";

const PlayerPage = function () {
  return (
    <div className="mb-4 w-full">
      <Breadcrumb className="mb-4">
        <Breadcrumb.Item>
          <div className="flex items-center gap-x-3">
            <span className="dark:text-white">
              <Link to="/">Home</Link>
            </span>
          </div>
        </Breadcrumb.Item>
        <Breadcrumb.Item>
          <div className="flex items-center gap-x-3">
            <span className="dark:text-white">
              <Link to="/team">Team name</Link>
            </span>
          </div>
        </Breadcrumb.Item>
        <Breadcrumb.Item>Player name</Breadcrumb.Item>
      </Breadcrumb>

      <h1 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
        Player Details
      </h1>

      <List unstyled className="p-4">
        <List.Item>Average score: 38.5</List.Item>
        <List.Item>Total games played: 7</List.Item>
      </List>
    </div>
  );
};

export default PlayerPage;
