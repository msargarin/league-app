import { Breadcrumb } from "flowbite-react";
import { Link } from "react-router-dom";
import TeamRoster from "../components/TeamRoster";

const TeamPage = function () {
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
        <Breadcrumb.Item>Team name</Breadcrumb.Item>
      </Breadcrumb>

      <h1 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
        Team Details
      </h1>

      <p className="mt-4 mb-4 dark:text-white">
        <span>Average score: </span>
        <span>98.2</span>
      </p>

      <TeamRoster />
    </div>
  );
};

export default TeamPage;
