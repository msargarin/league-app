import { Breadcrumb } from "flowbite-react";
import { Link, useParams } from "react-router-dom";
import TeamRoster from "../components/TeamRoster";
import { useEffect, useState } from "react";
import { callApi } from "../utils/api";

const TeamPage = function ({ user }) {
  const { teamId } = useParams();

  const [team, setTeam] = useState(null);

  useEffect(() => {
    callApi("http://localhost:8000/team/" + teamId, user.token, setTeam);
  }, []);

  return team ? (
    <div className="mb-4 w-full">
      <Breadcrumb className="mb-4">
        <Breadcrumb.Item>
          <div className="flex items-center gap-x-3">
            <span className="dark:text-white">
              <Link to="/">Home</Link>
            </span>
          </div>
        </Breadcrumb.Item>
        <Breadcrumb.Item>{team.name}</Breadcrumb.Item>
      </Breadcrumb>

      <h1 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
        {team.name}
      </h1>

      <p className="mt-4 mb-4 dark:text-white">
        <span>Average score: </span>
        <span>{team.average_score}</span>
      </p>

      <TeamRoster players={team.players} />
    </div>
  ) : (
    <span>Loading team data ...</span>
  );
};

export default TeamPage;
