import { Table, Alert } from "flowbite-react";
import { HiInformationCircle } from "react-icons/hi";
import { useNavigate } from "react-router";

const TeamRoster = function () {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/player");
  };

  return (
    <div className="shadow-lg m-1 mt-2 border-t-2">
      <h2 className="font-semibold text-gray-900 dark:text-white sm:text-xl p-4 pb-0">
        Roster
      </h2>

      <Alert color="info" icon={HiInformationCircle} className="m-4">
        <span className="text-medium">
          Click on a player to view more details
        </span>
      </Alert>

      <Table className="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
        <Table.Head className="bg-gray-100 dark:bg-gray-700">
          <Table.HeadCell>Name</Table.HeadCell>
          <Table.HeadCell>Average Score</Table.HeadCell>
          <Table.HeadCell>Games Played</Table.HeadCell>
        </Table.Head>

        <Table.Body className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-800">
          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Neil Sims
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              43.5
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              8
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Roberta Casas
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              32.1
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              4
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Michael Gough
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              13.2
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              4
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Jese Leos
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              9.0
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              2
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Bonnie Green
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              0
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              1
            </Table.Cell>
          </Table.Row>
          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Thomas Lean
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              24.2
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              6
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Helene Engels
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              12.4
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              7
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Lana Byrd
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              19.4
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              7
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Leslie Livingston
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              11.3
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              8
            </Table.Cell>
          </Table.Row>

          <Table.Row
            className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
            onClick={handleClick}
          >
            <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
              <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                <div className="text-base font-semibold text-gray-900 dark:text-white">
                  Robert Brown
                </div>
              </div>
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              35.9
            </Table.Cell>
            <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
              6
            </Table.Cell>
          </Table.Row>
        </Table.Body>
      </Table>
    </div>
  );
};

export default TeamRoster;
