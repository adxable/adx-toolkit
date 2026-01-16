---
name: react-forms
description: React form patterns using Zod validation and react-hook-form. Use when creating forms, implementing validation, building filter forms, or working with form configurations.
---

# React Forms

Comprehensive guide for building forms with Zod validation and react-hook-form.

## When to Use This Skill

- Creating new forms
- Adding form validation with Zod
- Building filter forms with auto-submit
- Configuring form field types
- Working with external submit buttons (dialog forms)
- Setting up form sections and layouts

---

## Quick Start - Form Checklist

- [ ] Define Zod schema for validation
- [ ] Set up default values matching schema
- [ ] Use react-hook-form for form state
- [ ] Add `onSubmit` handler
- [ ] For dialogs: use external submit with hidden submit button

---

## Basic Form Pattern

```typescript
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'sonner';

// 1. Zod schema for validation
const formSchema = z.object({
    name: z.string().min(3, 'Name must be at least 3 characters'),
    email: z.string().email('Invalid email address'),
    parentId: z.string().optional(),
    isCritical: z.boolean(),
    additionalInfo: z.string().optional(),
});

type FormData = z.infer<typeof formSchema>;

// 2. Default values
const defaultValues: FormData = {
    name: '',
    email: '',
    parentId: '',
    isCritical: false,
    additionalInfo: '',
};

// 3. Component
export const MyForm: React.FC = () => {
    const form = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues,
    });

    const handleSubmit = async (data: FormData) => {
        try {
            await api.submitForm(data);
            toast.success('Form submitted successfully');
        } catch (error) {
            toast.error('Failed to submit form');
        }
    };

    return (
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <div>
                <label htmlFor="name">Name *</label>
                <input
                    id="name"
                    {...form.register('name')}
                    className="w-full rounded border p-2"
                />
                {form.formState.errors.name && (
                    <p className="text-red-500 text-sm">
                        {form.formState.errors.name.message}
                    </p>
                )}
            </div>

            <div>
                <label htmlFor="email">Email *</label>
                <input
                    id="email"
                    type="email"
                    {...form.register('email')}
                    className="w-full rounded border p-2"
                />
                {form.formState.errors.email && (
                    <p className="text-red-500 text-sm">
                        {form.formState.errors.email.message}
                    </p>
                )}
            </div>

            <div className="flex items-center gap-2">
                <input
                    id="isCritical"
                    type="checkbox"
                    {...form.register('isCritical')}
                />
                <label htmlFor="isCritical">Is Critical</label>
            </div>

            <div>
                <label htmlFor="additionalInfo">Additional Info</label>
                <textarea
                    id="additionalInfo"
                    {...form.register('additionalInfo')}
                    rows={4}
                    className="w-full rounded border p-2"
                />
            </div>

            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
                Submit
            </button>
        </form>
    );
};
```

---

## External Submit Button (For Dialogs)

When you need to control the submit button externally (e.g., in a dialog footer):

```typescript
import { useRef } from 'react';

export const MyFormWithExternalSubmit: React.FC = () => {
    const submitRef = useRef<HTMLButtonElement>(null);

    const form = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues,
    });

    const handleSubmit = async (data: FormData) => {
        try {
            await api.submitForm(data);
            toast.success('Form submitted successfully');
        } catch (error) {
            toast.error('Failed to submit form');
        }
    };

    const handleExternalSubmit = () => {
        submitRef.current?.click();
    };

    return (
        <div>
            <form onSubmit={form.handleSubmit(handleSubmit)}>
                {/* Form fields here */}
                <button type="submit" ref={submitRef} className="hidden" />
            </form>

            {/* External submit button - e.g., in dialog footer */}
            <Button onClick={handleExternalSubmit} variant="primary">
                Save Changes
            </Button>
        </div>
    );
};
```

---

## Filter Forms with Debounce

### Auto-Submitting Filters

```typescript
import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useDebounce } from 'use-debounce';

interface FiltersForm {
    id: string;
    name: string;
    isCritical: boolean;
}

const defaultValues: FiltersForm = {
    id: '',
    name: '',
    isCritical: false,
};

export const MyFilters: React.FC<{ onApply: (filters: FiltersForm) => void }> = ({
    onApply,
}) => {
    const form = useForm<FiltersForm>({ defaultValues });
    const formValues = form.watch();

    // Debounce text inputs
    const [debouncedValues] = useDebounce(formValues, 300);

    // Auto-apply on change
    useEffect(() => {
        onApply(debouncedValues);
    }, [debouncedValues, onApply]);

    return (
        <div className="space-y-4 p-4">
            <div>
                <label>ID</label>
                <input {...form.register('id')} className="w-full rounded border p-2" />
            </div>

            <div>
                <label>Name</label>
                <input {...form.register('name')} className="w-full rounded border p-2" />
            </div>

            <div className="flex items-center gap-2">
                <input type="checkbox" {...form.register('isCritical')} />
                <label>Critical Only</label>
            </div>
        </div>
    );
};
```

---

## Zod Validation Patterns

### Common Validation Rules

```typescript
import { z } from 'zod';

const formSchema = z.object({
    // Required string
    name: z.string().min(1, 'Required'),

    // Email
    email: z.string().email('Invalid email'),

    // Optional string
    description: z.string().optional(),

    // Number with range
    quantity: z.number().min(1).max(100),

    // Boolean
    isActive: z.boolean(),

    // Optional with default
    status: z.string().default('draft'),

    // Enum
    priority: z.enum(['low', 'medium', 'high']),

    // Conditional validation
    endDate: z.string().optional(),
}).refine(
    (data) => !data.endDate || new Date(data.endDate) > new Date(),
    { message: 'End date must be in the future', path: ['endDate'] }
);
```

---

## Key Benefits

- **Type-safe** - Full TypeScript support with Zod
- **Declarative validation** - Schema-based validation rules
- **Flexible** - External submit, dynamic configs, filter forms
- **Performance** - Only re-renders on field changes

---

## See Also

- `react-performance` skill - Optimizing form re-renders
- `zod-validation` skill - Advanced Zod patterns
