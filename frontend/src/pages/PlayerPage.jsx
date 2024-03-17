import { Breadcrumb, List } from "flowbite-react";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { callApi } from "../utils/api";

const PlayerPage = function ({ user }) {
  const { playerId } = useParams();

  const [player, setTeam] = useState(null);

  useEffect(() => {
    callApi("http://localhost:8000/player/" + playerId, user.token, setTeam);
  }, []);

  return player ? (
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
              <Link to={`/team/${player.team_pk}`}>{player.team}</Link>
            </span>
          </div>
        </Breadcrumb.Item>
        <Breadcrumb.Item>{player.name}</Breadcrumb.Item>
      </Breadcrumb>

      <h1 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
        {player.name}
      </h1>

      <List unstyled className="p-4">
        <List.Item>Average score: {player.average_score}</List.Item>
        <List.Item>Total games played: {player.total_games_played}</List.Item>
      </List>
    </div>
  ) : (
    <span>Loading player data ...</span>
  );
};

export default PlayerPage;
