import "../assets/bracket.css";
import { useNavigate } from "react-router";

const Bracket = function ({ user, games }) {
  const navigate = useNavigate();

  const handleClick = (id) => {
    navigate("/team/" + id);
  };

  return (
    <div className="bracket-theme bracket-theme-dark overflow-auto m-auto mt-4 rounded">
      <div className="bracket xl:justify-center">
        {games ? (
          games.map((round, i) => {
            return (
              <div className="column" key={i}>
                {round.map((game) => {
                  return (
                    <div
                      key={game.id}
                      className={`match ${
                        user.role != "player" ? "cursor-pointer" : ""
                      } ${
                        game.team_a_score > game.team_b_score
                          ? "winner-top"
                          : "winner-bottom"
                      }
                      `}
                    >
                      <div
                        className="match-top team"
                        onClick={
                          user.role != "player"
                            ? () => handleClick(game.team_a_pk)
                            : () => {}
                        }
                      >
                        <span className="name">{game.team_a}</span>
                        <span className="score">{game.team_a_score}</span>
                      </div>
                      <div
                        className="match-bottom team"
                        onClick={
                          user.role != "player"
                            ? () => handleClick(game.team_b_pk)
                            : () => {}
                        }
                      >
                        <span className="name">{game.team_b}</span>
                        <span className="score">{game.team_b_score}</span>
                      </div>
                      <div className="match-lines">
                        <div className="line one"></div>
                        <div className="line two"></div>
                      </div>
                      <div className="match-lines alt">
                        <div className="line one"></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            );
          })
        ) : (
          <span className="text-white p-2">Loading games ...</span>
        )}
      </div>
    </div>
  );
};

export default Bracket;
