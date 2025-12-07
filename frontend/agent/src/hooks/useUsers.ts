// Example hook using the generic useApi wrapper + UsersService
import { useApi } from './useApi';
import { UsersService, User } from '../services/users';

export function useUsers() {
  const list = useApi<User[]>(UsersService.list, []);
  const create = async (payload: Omit<User, 'id'|'created_at'>) => {
    const newUser = await UsersService.create(payload);
    // Optimistically update list cache if it's already loaded
    if (list.data) list.setData([newUser, ...list.data]);
    return newUser;
  };
  return { list, create };
}
