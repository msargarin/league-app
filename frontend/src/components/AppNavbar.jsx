import { DarkThemeToggle, Navbar, Dropdown, Avatar } from "flowbite-react";

const AppNavbar = function ({ user, setUser }) {
  const handleLogout = () => {
    setUser(null);
  };

  return (
    <Navbar fluid>
      <Navbar.Brand href="/">
        <img alt="" src="/images/logo.svg" className="mr-3 h-6 sm:h-8" />
        <span className="self-center whitespace-nowrap text-2xl font-semibold dark:text-white">
          League App
        </span>
      </Navbar.Brand>
      <div className="flex md:order-2 gap-2 pr-4">
        <DarkThemeToggle />
        <Dropdown
          arrowIcon={false}
          inline
          label={
            <Avatar
              alt="User settings"
              img="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
              rounded
            />
          }
        >
          <Dropdown.Header>
            <span className="block text-sm">{user.name}</span>
            <span className="block truncate text-sm font-medium">
              {user.role}
              {user.role == "admin" ? "" : `at ${user.team}`}
            </span>
          </Dropdown.Header>
          <Dropdown.Item onClick={handleLogout}>Sign out</Dropdown.Item>
        </Dropdown>
        <Navbar.Toggle />
      </div>
    </Navbar>
  );
};

export default AppNavbar;
