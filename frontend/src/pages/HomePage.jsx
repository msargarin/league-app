import { Alert, Breadcrumb } from "flowbite-react";
import { HiInformationCircle } from "react-icons/hi";
import Bracket from "../components/Bracket";

const HomePage = function ({ user }) {
  return (
    <div className="mb-4 w-full">
      <Breadcrumb className="mb-4">
        <Breadcrumb.Item>
          <div className="flex items-center gap-x-3">
            <span className="dark:text-white">Home</span>
          </div>
        </Breadcrumb.Item>
      </Breadcrumb>

      <h1 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
        Tournament Brackets
      </h1>

      {user.role == "admin" || user.role == "coach" ? (
        <Alert color="info" icon={HiInformationCircle} className="mt-4">
          <span className="text-medium">
            {user.role == "admin"
              ? "Click on a team to view their details"
              : "Click on your team to view more information"}
          </span>
        </Alert>
      ) : (
        ""
      )}

      <Bracket />
    </div>
  );
};

export default HomePage;
