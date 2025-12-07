// Example "Users" service showing how to define typed endpoints.
import { get, post, put, del } from '../lib/http';

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface CreateUserInput {
  email: string;
  name: string;
  password?: string; // optional if backend auto-generates
}

export const UsersService = {
  list: () => get<User[]>('/users'),
  getById: (id: string) => get<User>(`/users/${id}`),
  create: (payload: CreateUserInput) => post<User>('/users', payload),
  update: (id: string, payload: Partial<CreateUserInput>) => put<User>(`/users/${id}`, payload),
  remove: (id: string) => del<{ ok: true }>(`/users/${id}`),
};
