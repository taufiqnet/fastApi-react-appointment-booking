"use client";

import axios from "axios";
import { Eye, EyeOff } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Register() {
  const router = useRouter();

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    mobile_number: "",
    password: "",
    user_type: "patient",
    division: "",
    district: "",
    thana: "",
    license_number: "",
    experience_years: "",
    consultation_fee: "",
    available_timeslots: "",
  });

  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [errors, setErrors] = useState<string[]>([]);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [divisions, setDivisions] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [thanas, setThanas] = useState<string[]>([]);

  useEffect(() => {
    setDivisions(["Dhaka", "Chattogram", "Khulna"]);
  }, []);

  useEffect(() => {
    const mapping: any = {
      Dhaka: ["Dhaka", "Gazipur"],
      Chattogram: ["Ctg City"],
      Khulna: ["Khulna City"],
    };
    setDistricts(mapping[form.division] || []);
    setForm((f) => ({ ...f, district: "", thana: "" }));
  }, [form.division]);

  useEffect(() => {
    const mapping: any = {
      Dhaka: ["Dhanmondi", "Mirpur"],
      Gazipur: ["Tongi"],
      "Ctg City": ["Kotwali"],
      "Khulna City": ["Khalishpur"],
    };
    setThanas(mapping[form.district] || []);
    setForm((f) => ({ ...f, thana: "" }));
  }, [form.district]);

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleImage = (e: any) => {
    const file = e.target.files[0];
    if (file) {
      const validTypes = ["image/jpeg", "image/png"];
      if (!validTypes.includes(file.type)) {
        setErrors(["❌ Only JPEG/PNG images are allowed"]);
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        setErrors(["❌ Image must be less than 5MB"]);
        return;
      }
      setProfileImage(file);
      setErrors([]);
    }
  };

  const validateForm = async () => {
    const errorList: string[] = [];

    if (!form.full_name) errorList.push("Full name is required");
    if (!form.email) errorList.push("Email is required");
    if (!form.mobile_number.match(/^\+88\d{11}$/)) errorList.push("Invalid mobile number (+88 format)");
    if (!form.password.match(/^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/)) {
      errorList.push("Password must contain: 8+ chars, 1 uppercase, 1 number, 1 special char");
    }

    if (!["admin", "doctor", "patient"].includes(form.user_type))
      errorList.push("Invalid user type");

    if (!form.division || !form.district || !form.thana)
      errorList.push("Complete address (division, district, thana) is required");

    if (!profileImage) errorList.push("Profile image is required");

    if (form.user_type === "doctor") {
      if (!form.license_number) errorList.push("License number required for doctors");
      if (!form.experience_years) errorList.push("Experience years required");
      if (!form.consultation_fee) errorList.push("Consultation fee required");
      if (!form.available_timeslots.match(/^\d{2}:\d{2}-\d{2}:\d{2}$/))
        errorList.push("Available timeslot format must be like 10:00-11:00");
    }

    try {
      const res = await axios.post("http://localhost:8000/api/v1/auth/check-email", {
        email: form.email,
        mobile_number: form.mobile_number,
      });
      if (!res.data.ok) errorList.push("Email or mobile already exists");
    } catch (e) {}

    setErrors(errorList);
    return errorList.length === 0;
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setIsLoading(true);
    if (!(await validateForm())) {
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    for (const key in form) formData.append(key, (form as any)[key]);
    if (profileImage) formData.append("profile_image", profileImage);

    try {
      await axios.post("http://localhost:8000/api/v1/auth/register", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("✅ Registration successful!");
      router.push("/auth/login");
    } catch (err: any) {
<<<<<<< HEAD
      const errorDetail = err?.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        setErrors(errorDetail.map((e: any) => e.msg));
      } else {
        setErrors([errorDetail || "Registration failed. Please try again."]);
      }
=======
      const errorDetail = err?.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        setErrors(errorDetail.map((e: any) => e.msg));
      } else {
        setErrors([errorDetail || "Registration failed. Please try again."]);
      }
>>>>>>> 32db5770376e2b4a45d4de9155b1b355957b5b69
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-blue-600 p-6 text-center">
          <h1 className="text-2xl font-bold text-white">Create Your Account</h1>
          <p className="text-blue-100 mt-1">Join our healthcare platform today</p>
        </div>

        {/* Form */}
        <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          {errors.length > 0 && (
            <div className="md:col-span-2 bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded">
              <div className="font-medium">Please fix these issues:</div>
              <ul className="mt-1 list-disc list-inside space-y-1">
                {errors.map((err, idx) => (
                  <li key={idx}>{err}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              name="full_name"
              placeholder="John Doe"
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              name="email"
              type="email"
              placeholder="your@email.com"
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Mobile (+880)</label>
            <input
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              name="mobile_number"
              placeholder="+8801XXXXXXXXX"
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <div className="relative">
              <input
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition pr-10"
                name="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                onChange={handleChange}
                required
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">User Type</label>
            <select
              name="user_type"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              onChange={handleChange}
            >
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Profile Image</label>
            <input
              type="file"
              accept=".png,.jpeg,.jpg"
              onChange={handleImage}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              required
            />
          </div>

          {form.user_type === "doctor" && (
            <>
              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">License Number</label>
                <input
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                  name="license_number"
                  placeholder="MED123456"
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">Experience (Years)</label>
                <input
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                  name="experience_years"
                  type="number"
                  placeholder="5"
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">Consultation Fee</label>
                <input
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                  name="consultation_fee"
                  type="number"
                  placeholder="500"
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">Available Timeslot</label>
                <input
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                  name="available_timeslots"
                  placeholder="10:00-11:00"
                  onChange={handleChange}
                />
              </div>
            </>
          )}

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Division</label>
            <select
              name="division"
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              value={form.division}
              required
            >
              <option value="">Select Division</option>
              {divisions.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">District</label>
            <select
              name="district"
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              value={form.district}
              required
            >
              <option value="">Select District</option>
              {districts.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Thana</label>
            <select
              name="thana"
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              value={form.thana}
              required
            >
              <option value="">Select Thana</option>
              {thanas.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>

          <div className="md:col-span-2">
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition ${isLoading ? "opacity-70 cursor-not-allowed" : ""}`}
              onClick={handleSubmit}
            >
              {isLoading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating account...
                </span>
              ) : (
                "Register Now"
              )}
            </button>
          </div>

          <div className="md:col-span-2 text-center text-sm text-gray-600">
            Already have an account?{" "}
            <a href="/auth/login" className="font-medium text-blue-600 hover:text-blue-500">
              Sign in
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}