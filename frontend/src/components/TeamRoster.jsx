import { Table, Alert } from "flowbite-react";
import { HiInformationCircle } from "react-icons/hi";
import { useNavigate } from "react-router";

const TeamRoster = function ({ players }) {
  const navigate = useNavigate();

  const handleClick = (playerId) => {
    navigate("/player/" + playerId);
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
          {players ? (
            players.map((player) => {
              return (
                <Table.Row
                  key={player.pk}
                  className="hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer"
                  onClick={() => handleClick(player.pk)}
                >
                  <Table.Cell className="mr-12 flex items-center space-x-6 whitespace-nowrap p-4 lg:mr-0">
                    <div className="text-sm font-normal text-gray-500 dark:text-gray-400">
                      <div className="text-base font-semibold text-gray-900 dark:text-white">
                        {player.name}
                      </div>
                    </div>
                  </Table.Cell>
                  <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
                    {player.average_score}
                  </Table.Cell>
                  <Table.Cell className="whitespace-nowrap p-4 text-base font-medium text-gray-900 dark:text-white">
                    {player.total_games_played}
                  </Table.Cell>
                </Table.Row>
              );
            })
          ) : (
            <span>Loading players ...</span>
          )}
        </Table.Body>
      </Table>
    </div>
  );
};

export default TeamRoster;
