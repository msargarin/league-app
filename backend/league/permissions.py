from rest_framework import permissions

ACCOUNT_LEVEL_PLAYER = 'player'
ACCOUNT_LEVEL_COACH = 'coach'
ACCOUNT_LEVEL_ADMIN = 'admin'
ACCOUNT_LEVELS = {
    ACCOUNT_LEVEL_PLAYER: 0,
    ACCOUNT_LEVEL_COACH: 1,
    ACCOUNT_LEVEL_ADMIN: 2
}


class RoleBasedPermission(permissions.BasePermission):
    '''
    Permissions based on a user's role
    '''
    min_role = None

    def has_permission(self, request, view):
        # Only allow access to a specified role
        return hasattr(request.user, 'role') and ACCOUNT_LEVELS[request.user.role.lower()] >= self.min_role


class IsAtLeastPlayer(RoleBasedPermission):
    '''
    Permission to only allow access to players
    '''
    min_role = ACCOUNT_LEVELS[ACCOUNT_LEVEL_PLAYER]


class IsAtLeastCoach(RoleBasedPermission):
    '''
    Permission to only allow access to coaches
    '''
    min_role = ACCOUNT_LEVELS[ACCOUNT_LEVEL_COACH]


class TeamCoachOrAdmin(permissions.BasePermission):
    '''
    Permission to only allow access for a team's coach or an admin
    '''
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role'):
            # Admin always has access
            if request.user.role.lower() == ACCOUNT_LEVEL_ADMIN:
                return True

            # Coach only has access to his team
            if request.user.role.lower() == ACCOUNT_LEVEL_COACH \
                    and obj.name == request.user.team and obj.coach.name == request.user.name:
                return True

        return False

class PlayersTeamCoachOrAdmin(permissions.BasePermission):
    '''
    Permission to only allow access for the player's coach or an admin
    '''
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role'):
            # Admin always has access
            if request.user.role.lower() == ACCOUNT_LEVEL_ADMIN:
                return True

            # Coach only has access to his team
            if request.user.role.lower() == ACCOUNT_LEVEL_COACH \
                    and obj.team.name == request.user.team and obj.team.coach.name == request.user.name:
                return True

        return False
