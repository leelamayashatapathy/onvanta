import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../../../components/ui/Button";
import { Input } from "../../../components/ui/Input";
import { Card } from "../../../components/ui/Card";
import { useLogin } from "../hooks";

const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormValues = z.infer<typeof schema>;

export function LoginPage() {
  const navigate = useNavigate();
  const { mutateAsync, isPending, isSuccess, error } = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: "onChange",
    defaultValues: {
      email: "",
      password: "",
    },
  });

  useEffect(() => {
    if (isSuccess) {
      navigate("/app/dashboard", { replace: true });
    }
  }, [isSuccess, navigate]);

  const onSubmit = async (values: FormValues) => {
    await mutateAsync(values);
  };

  return (
    <Card className="p-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold text-slate-900">Sign in</h2>
        <p className="text-sm text-slate-600">Access your vendor compliance workspace.</p>
      </div>

      <form className="mt-6 space-y-4" onSubmit={handleSubmit(onSubmit)}>
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700" htmlFor="email">
            Work email
          </label>
          <Input
            id="email"
            type="email"
            placeholder="you@company.com"
            error={Boolean(errors.email)}
            {...register("email")}
          />
          {errors.email ? (
            <p className="text-xs text-red-600">{errors.email.message}</p>
          ) : null}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-slate-700" htmlFor="password">
              Password
            </label>
            <Link className="text-xs font-medium text-blue-600" to="/forgot-password">
              Forgot password
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            placeholder="Enter your password"
            error={Boolean(errors.password)}
            {...register("password")}
          />
          {errors.password ? (
            <p className="text-xs text-red-600">{errors.password.message}</p>
          ) : null}
        </div>

        {error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
            Unable to sign in. Please check your credentials and try again.
          </div>
        ) : null}

        <Button type="submit" className="w-full" disabled={!isValid || isPending}>
          {isPending ? "Signing in..." : "Sign in"}
        </Button>
      </form>

      <div className="mt-6 rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-600">
        Demo access: use your internal credentials once connected to the backend.
      </div>
    </Card>
  );
}
