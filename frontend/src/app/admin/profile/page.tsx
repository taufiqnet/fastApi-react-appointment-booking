"use client";

import Layout from "@/components/Layout";
import { useAuth } from "@/context/AuthContext";

export default function AdminProfile() {
  const { user } = useAuth();

  return (
    <Layout>
      <div className="p-6">
        <div className="flex items-center space-x-4">
          <img
            src={user?.profile_image ? `data:image/png;base64,${user.profile_image}` : "/default-avatar.png"}
            alt="Profile"
            className="w-24 h-24 rounded-full"
          />
          <div>
            <h1 className="text-2xl font-bold">👨‍💼 {user?.full_name}</h1>
            <p>{user?.email}</p>
          </div>
        </div>
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Admin Dashboard</h2>
          <p>Manage appointments and doctors here.</p>
        </div>
      </div>
    </Layout>
  );
}
