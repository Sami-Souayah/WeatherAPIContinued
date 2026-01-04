import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../api/client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";
import { User, Lock } from "lucide-react";




export default function CreateUser() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();
  const [strength, setStrength] = useState(0);


  const evaluatestrength = (pass) => {
    if (!pass){
        setStrength(0);
        return;
    }
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(pass)) score++;
    console.log("evaluatestrength:", pass, "=>", score);
    setStrength(score);
  };


  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const res = await apiRequest("/user/create", {
        method: "POST",
        body: JSON.stringify({ username, password, confirmPassword }),
      });
      setSuccess("Account created successfully!");
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
        if (err.error) setError(err.error);
        else setError(err.message || "Failed to create account.");
    }
  };

  const strengthLabel = ["Too short", "Weak", "Fair", "Good", "Strong"];
  const strengthColors = ["bg-gray-300", "bg-red-400", "bg-yellow-400", "bg-blue-400", "bg-green-500"];


   return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="w-96 shadow-lg rounded-2xl backdrop-blur-md bg-white/80 border border-white/20">
          <CardContent className="p-6">
            <h2 className="text-2xl font-semibold text-center mb-6 text-gray-800">
              Create Account
            </h2>

            <form onSubmit={handleCreate} className="space-y-4">
              {/* Username Input */}
              <div className="relative">
                <User className="absolute left-3 top-3 text-gray-400" size={18} />
                <Input
                  className="pl-10"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>

              {/* Password Input */}
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={18} />
                <Input
                  type="password"
                  className="pl-10"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => {
                    const val = e.target.value
                    setPassword(val);
                    evaluatestrength(val);

                  }}
                />
              </div>

              {/* Password Strength Indicator */}
              {password && (
                <div className="mt-1">
                  <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${strengthColors[strength]}`}
                      style={{ width: `${(strength / 4) * 100}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-1 text-right">
                    {strengthLabel[strength]}
                  </p>
                </div>
              )}

              {/* Confirm Password Input */}
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={18} />
                <Input
                  type="password"
                  className="pl-10"
                  placeholder="Confirm Password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>

              {/* Error / Success Feedback */}
              {error && (
                <p className="text-red-500 text-sm text-center bg-red-50 py-1 rounded">
                  {error}
                </p>
              )}
              {success && (
                <p className="text-green-600 text-sm text-center bg-green-50 py-1 rounded">
                  {success}
                </p>
              )}

              {/* Buttons */}
              <Button
                type="submit"
                className="w-full bg-blue-500 hover:bg-blue-600 transition-all"
              >
                Create Account
              </Button>

              <Button
                type="button"
                onClick={() => navigate("/")}
                variant="outline"
                className="w-full mt-2 border-blue-500 text-blue-600 hover:bg-blue-50"
              >
                Back to Login
              </Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
