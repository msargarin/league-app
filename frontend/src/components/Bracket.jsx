import "../assets/bracket.css";
import { useNavigate } from "react-router";

const Bracket = function () {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/team");
  };

  return (
    <div className="bracket-theme bracket-theme-dark overflow-auto m-auto mt-4 rounded">
      <div className="bracket xl:justify-center">
        {/* First Round */}
        <div className="column">
          {/* Matches always go in pairs */}
          {/* One Match */}
          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Orlando Jetsetters</span>
              <span className="score">2</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">D.C. Senators</span>
              <span className="score">1</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          {/* Another Match */}
          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">New Orleans Rockstars</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Denver Demon Horses</span>
              <span className="score">2</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">Chicago Pistons</span>
              <span className="score">0</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">Seattle Climbers</span>
              <span className="score">1</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Orlando Jetsetters</span>
              <span className="score">2</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">D.C. Senators</span>
              <span className="score">1</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">New Orleans Rockstars</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">New Orleans Rockstars</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">New Orleans Rockstars</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>
        </div>

        {/* Second Round */}
        <div className="column">
          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Orlando Jetsetters</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Denver Demon Horses</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Denver Demon Horses</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">Denver Demon Horses</span>
              <span className="score">1</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>
        </div>

        {/* Third Round */}
        <div className="column">
          <div className="match winner-top">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">3</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>

          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">3</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>
        </div>

        {/* Fourth Round */}
        <div className="column">
          <div className="match winner-bottom">
            <div className="match-top team" onClick={handleClick}>
              <span className="name">West Virginia Runners</span>
              <span className="score">3</span>
            </div>
            <div className="match-bottom team" onClick={handleClick}>
              <span className="name">San Francisco Porters</span>
              <span className="score">2</span>
            </div>
            <div className="match-lines">
              <div className="line one"></div>
              <div className="line two"></div>
            </div>
            <div className="match-lines alt">
              <div className="line one"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Bracket;
